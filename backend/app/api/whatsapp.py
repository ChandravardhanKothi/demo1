"""
WhatsApp API integration for sending advisories and notifications.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json
from typing import Optional
import os

from app.core.database import get_db
from app.models.user import User
from app.models.advisory import Advisory
from app.core.config import settings
from app.services.tts_service import TTSService

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])

# Initialize Twilio client
twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

# Initialize TTS service
tts_service = TTSService()


@router.post("/send")
async def send_whatsapp_message(
    user_id: int,
    message: str,
    language: str = "en",
    include_voice: bool = False,
    db: Session = Depends(get_db)
):
    """
    Send WhatsApp message to user.
    
    Args:
        user_id: User ID
        message: Message content
        language: Message language (en, hi, te, ta)
        include_voice: Whether to include voice message
        db: Database session
        
    Returns:
        Delivery status
    """
    try:
        # Get user details
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.whatsapp_enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="WhatsApp notifications disabled for this user"
            )
        
        # Format phone number for WhatsApp
        phone_number = f"whatsapp:{user.phone_number}"
        
        # Send text message
        message_obj = twilio_client.messages.create(
            body=message,
            from_=settings.twilio_whatsapp_number,
            to=phone_number
        )
        
        # Generate voice message if requested
        voice_url = None
        if include_voice:
            voice_file = await tts_service.generate_voice(
                text=message,
                language=language,
                user_id=user_id
            )
            
            if voice_file:
                # Upload to a public URL (in production, use proper file storage)
                voice_url = f"https://your-domain.com/uploads/{os.path.basename(voice_file)}"
                
                # Send voice message
                voice_message = twilio_client.messages.create(
                    media_url=[voice_url],
                    from_=settings.twilio_whatsapp_number,
                    to=phone_number
                )
        
        # Save advisory record
        advisory = Advisory(
            user_id=user_id,
            title="WhatsApp Advisory",
            content=message,
            advisory_type="whatsapp",
            language=language,
            voice_file_path=voice_file if include_voice else None,
            whatsapp_sent=True
        )
        
        db.add(advisory)
        db.commit()
        
        return {
            "success": True,
            "message_sid": message_obj.sid,
            "voice_url": voice_url,
            "delivered": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send WhatsApp message: {str(e)}"
        )


@router.post("/voice")
async def send_voice_message(
    user_id: int,
    text: str,
    language: str = "en",
    db: Session = Depends(get_db)
):
    """
    Send voice message via WhatsApp.
    
    Args:
        user_id: User ID
        text: Text to convert to speech
        language: Language for TTS
        db: Database session
        
    Returns:
        Voice message delivery status
    """
    try:
        # Get user details
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Generate voice file
        voice_file = await tts_service.generate_voice(
            text=text,
            language=language,
            user_id=user_id
        )
        
        if not voice_file:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate voice file"
            )
        
        # Upload to public URL (in production, use proper file storage)
        voice_url = f"https://your-domain.com/uploads/{os.path.basename(voice_file)}"
        
        # Send voice message
        phone_number = f"whatsapp:{user.phone_number}"
        message_obj = twilio_client.messages.create(
            media_url=[voice_url],
            from_=settings.twilio_whatsapp_number,
            to=phone_number
        )
        
        return {
            "success": True,
            "message_sid": message_obj.sid,
            "voice_url": voice_url,
            "delivered": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send voice message: {str(e)}"
        )


@router.post("/webhook")
async def whatsapp_webhook(request):
    """
    Handle incoming WhatsApp messages.
    
    Args:
        request: FastAPI request object
        
    Returns:
        TwiML response
    """
    try:
        # Parse incoming message
        form_data = await request.form()
        
        message_body = form_data.get('Body', '')
        sender_number = form_data.get('From', '')
        
        # Create TwiML response
        response = MessagingResponse()
        
        # Process different message types
        if message_body.lower() in ['weather', 'weather update', 'weather info']:
            response.message("🌤️ Weather information coming soon! Please use the web dashboard for now.")
        
        elif message_body.lower() in ['market', 'prices', 'market prices']:
            response.message("📈 Market prices coming soon! Please use the web dashboard for now.")
        
        elif message_body.lower() in ['help', 'commands']:
            help_text = """
🌾 *Agricultural Advisory System*

Available commands:
• weather - Get weather information
• market - Get market prices  
• disease - Upload crop image for disease detection
• help - Show this help message

For full features, visit our web dashboard!
            """
            response.message(help_text)
        
        elif message_body.lower() in ['disease', 'detect', 'crop image']:
            response.message("📷 Please upload a crop image for disease detection. This feature will be available soon!")
        
        else:
            response.message("🤖 Thanks for your message! For full features, please visit our web dashboard or type 'help' for available commands.")
        
        return str(response)
        
    except Exception as e:
        # Return error response
        response = MessagingResponse()
        response.message("Sorry, there was an error processing your message. Please try again later.")
        return str(response)


@router.get("/status/{message_sid}")
async def get_message_status(message_sid: str):
    """
    Get WhatsApp message delivery status.
    
    Args:
        message_sid: Twilio message SID
        
    Returns:
        Message status
    """
    try:
        message = twilio_client.messages(message_sid).fetch()
        
        return {
            "success": True,
            "sid": message.sid,
            "status": message.status,
            "date_sent": message.date_sent.isoformat() if message.date_sent else None,
            "error_code": message.error_code,
            "error_message": message.error_message
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get message status: {str(e)}"
        )


@router.post("/broadcast")
async def broadcast_message(
    message: str,
    language: str = "en",
    user_ids: Optional[list] = None,
    db: Session = Depends(get_db)
):
    """
    Broadcast message to multiple users.
    
    Args:
        message: Message content
        language: Message language
        user_ids: List of user IDs (if None, sends to all users)
        db: Database session
        
    Returns:
        Broadcast results
    """
    try:
        # Get users to send to
        query = db.query(User).filter(User.whatsapp_enabled == True, User.is_active == True)
        
        if user_ids:
            query = query.filter(User.id.in_(user_ids))
        
        users = query.all()
        
        results = []
        successful = 0
        failed = 0
        
        for user in users:
            try:
                phone_number = f"whatsapp:{user.phone_number}"
                message_obj = twilio_client.messages.create(
                    body=message,
                    from_=settings.twilio_whatsapp_number,
                    to=phone_number
                )
                
                results.append({
                    "user_id": user.id,
                    "phone": user.phone_number,
                    "status": "sent",
                    "message_sid": message_obj.sid
                })
                successful += 1
                
                # Save advisory record
                advisory = Advisory(
                    user_id=user.id,
                    title="Broadcast Advisory",
                    content=message,
                    advisory_type="broadcast",
                    language=language,
                    whatsapp_sent=True
                )
                db.add(advisory)
                
            except Exception as e:
                results.append({
                    "user_id": user.id,
                    "phone": user.phone_number,
                    "status": "failed",
                    "error": str(e)
                })
                failed += 1
        
        db.commit()
        
        return {
            "success": True,
            "total_users": len(users),
            "successful": successful,
            "failed": failed,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to broadcast message: {str(e)}"
        )
