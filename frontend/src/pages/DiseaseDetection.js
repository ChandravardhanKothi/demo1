import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import styled from 'styled-components';
import { 
  Upload, 
  Camera, 
  AlertTriangle, 
  CheckCircle,
  Info,
  Download,
  RefreshCw
} from 'lucide-react';
import toast from 'react-hot-toast';
import axios from 'axios';

const DetectionContainer = styled.div`
  padding-top: 2rem;
`;

const Header = styled.div`
  margin-bottom: 2rem;
`;

const Title = styled.h1`
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
`;

const Subtitle = styled.p`
  color: #6b7280;
  font-size: 1rem;
`;

const ContentGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  
  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
`;

const UploadSection = styled.div`
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
`;

const SectionTitle = styled.h2`
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
`;

const DropzoneContainer = styled.div`
  border: 2px dashed ${props => props.isDragActive ? '#3b82f6' : '#d1d5db'};
  border-radius: 8px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: ${props => props.isDragActive ? '#eff6ff' : '#fafafa'};
  
  &:hover {
    border-color: #3b82f6;
    background-color: #eff6ff;
  }
`;

const UploadIcon = styled.div`
  width: 64px;
  height: 64px;
  margin: 0 auto 1rem;
  background-color: #f3f4f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
`;

const UploadText = styled.div`
  font-size: 1.125rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
`;

const UploadSubtext = styled.div`
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 1rem;
`;

const FileInput = styled.input`
  display: none;
`;

const CropSelector = styled.div`
  margin-top: 1.5rem;
`;

const SelectLabel = styled.label`
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
`;

const Select = styled.select`
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  background-color: white;
  cursor: pointer;
  
  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
`;

const AnalyzeButton = styled.button`
  width: 100%;
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  
  &:hover:not(:disabled) {
    background-color: #2563eb;
  }
  
  &:disabled {
    background-color: #9ca3af;
    cursor: not-allowed;
  }
`;

const ResultsSection = styled.div`
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
`;

const ImagePreview = styled.div`
  width: 100%;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1.5rem;
  background-color: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const PreviewImage = styled.img`
  width: 100%;
  height: 100%;
  object-fit: cover;
`;

const PlaceholderIcon = styled.div`
  color: #9ca3af;
  font-size: 3rem;
`;

const ResultCard = styled.div`
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border: 1px solid ${props => props.type === 'success' ? '#d1fae5' : props.type === 'warning' ? '#fef3c7' : '#fecaca'};
  background-color: ${props => props.type === 'success' ? '#ecfdf5' : props.type === 'warning' ? '#fffbeb' : '#fef2f2'};
`;

const ResultHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
`;

const ResultIcon = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: ${props => props.type === 'success' ? '#10b981' : props.type === 'warning' ? '#f59e0b' : '#ef4444'};
  color: white;
`;

const ResultTitle = styled.h3`
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
`;

const ResultContent = styled.div`
  color: #374151;
  line-height: 1.6;
`;

const ConfidenceBar = styled.div`
  width: 100%;
  height: 8px;
  background-color: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  margin: 1rem 0;
`;

const ConfidenceFill = styled.div`
  height: 100%;
  background-color: ${props => props.confidence > 0.7 ? '#10b981' : props.confidence > 0.5 ? '#f59e0b' : '#ef4444'};
  width: ${props => props.confidence * 100}%;
  transition: width 0.3s ease;
`;

const RecommendationsList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 1rem 0;
`;

const RecommendationItem = styled.li`
  padding: 0.5rem 0;
  color: #374151;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  
  &::before {
    content: '•';
    color: #3b82f6;
    font-weight: bold;
  }
`;

const LoadingSpinner = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #6b7280;
`;

function DiseaseDetection() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [cropType, setCropType] = useState('rice');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
      
      setResults(null);
      toast.success('Image uploaded successfully!');
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024 // 10MB
  });

  const analyzeImage = async () => {
    if (!selectedFile) {
      toast.error('Please select an image first');
      return;
    }

    setIsAnalyzing(true);
    
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('crop_type', cropType);

      const response = await axios.post('/api/disease/detect', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setResults(response.data);
        toast.success('Analysis completed successfully!');
      } else {
        toast.error('Analysis failed. Please try again.');
      }
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error('Failed to analyze image. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const resetAnalysis = () => {
    setSelectedFile(null);
    setImagePreview(null);
    setResults(null);
  };

  return (
    <DetectionContainer>
      <Header>
        <Title>Disease Detection</Title>
        <Subtitle>Upload crop images to detect diseases and get treatment recommendations.</Subtitle>
      </Header>

      <ContentGrid>
        <UploadSection>
          <SectionTitle>Upload Image</SectionTitle>
          
          <DropzoneContainer {...getRootProps()} isDragActive={isDragActive}>
            <FileInput {...getInputProps()} />
            <UploadIcon>
              <Camera size={32} />
            </UploadIcon>
            <UploadText>
              {isDragActive ? 'Drop the image here' : 'Drag & drop an image here'}
            </UploadText>
            <UploadSubtext>
              or click to browse files (JPEG, PNG, max 10MB)
            </UploadSubtext>
          </DropzoneContainer>

          <CropSelector>
            <SelectLabel>Select Crop Type</SelectLabel>
            <Select value={cropType} onChange={(e) => setCropType(e.target.value)}>
              <option value="rice">Rice</option>
              <option value="wheat">Wheat</option>
              <option value="maize">Maize</option>
              <option value="tomato">Tomato</option>
              <option value="potato">Potato</option>
            </Select>
          </CropSelector>

          <AnalyzeButton 
            onClick={analyzeImage} 
            disabled={!selectedFile || isAnalyzing}
          >
            {isAnalyzing ? (
              <>
                <RefreshCw size={16} className="animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Upload size={16} />
                Analyze Image
              </>
            )}
          </AnalyzeButton>

          {selectedFile && (
            <button 
              onClick={resetAnalysis}
              style={{
                width: '100%',
                marginTop: '1rem',
                padding: '0.5rem',
                background: 'none',
                border: '1px solid #d1d5db',
                borderRadius: '6px',
                color: '#6b7280',
                cursor: 'pointer',
                fontSize: '0.875rem'
              }}
            >
              Reset Analysis
            </button>
          )}
        </UploadSection>

        <ResultsSection>
          <SectionTitle>Analysis Results</SectionTitle>
          
          {imagePreview && (
            <ImagePreview>
              <PreviewImage src={imagePreview} alt="Uploaded crop" />
            </ImagePreview>
          )}

          {!imagePreview && !results && (
            <div style={{ textAlign: 'center', padding: '3rem 0', color: '#9ca3af' }}>
              <PlaceholderIcon>
                <Info size={48} />
              </PlaceholderIcon>
              <p>Upload an image to see analysis results</p>
            </div>
          )}

          {results && (
            <div>
              <ResultCard type={results.is_diseased ? 'warning' : 'success'}>
                <ResultHeader>
                  <ResultIcon type={results.is_diseased ? 'warning' : 'success'}>
                    {results.is_diseased ? <AlertTriangle size={20} /> : <CheckCircle size={20} />}
                  </ResultIcon>
                  <ResultTitle>
                    {results.disease} ({cropType.charAt(0).toUpperCase() + cropType.slice(1)})
                  </ResultTitle>
                </ResultHeader>
                <ResultContent>
                  <p>
                    <strong>Confidence:</strong> {(results.confidence * 100).toFixed(1)}%
                  </p>
                  <ConfidenceBar>
                    <ConfidenceFill confidence={results.confidence} />
                  </ConfidenceBar>
                  <p>
                    <strong>Image Quality:</strong> {results.image_quality}
                  </p>
                  <p>
                    <strong>Status:</strong> {results.is_diseased ? 'Disease Detected' : 'Healthy Crop'}
                  </p>
                </ResultContent>
              </ResultCard>

              {results.recommendations && results.recommendations.length > 0 && (
                <ResultCard type="info">
                  <ResultHeader>
                    <ResultIcon type="info">
                      <Info size={20} />
                    </ResultIcon>
                    <ResultTitle>Recommendations</ResultTitle>
                  </ResultHeader>
                  <ResultContent>
                    <RecommendationsList>
                      {results.recommendations.map((rec, index) => (
                        <RecommendationItem key={index}>{rec}</RecommendationItem>
                      ))}
                    </RecommendationsList>
                  </ResultContent>
                </ResultCard>
              )}

              {results.disease_info && Object.keys(results.disease_info).length > 0 && (
                <ResultCard type="info">
                  <ResultHeader>
                    <ResultIcon type="info">
                      <Info size={20} />
                    </ResultIcon>
                    <ResultTitle>Disease Information</ResultTitle>
                  </ResultHeader>
                  <ResultContent>
                    {results.disease_info.symptoms && (
                      <div style={{ marginBottom: '1rem' }}>
                        <strong>Symptoms:</strong>
                        <ul style={{ marginTop: '0.5rem', paddingLeft: '1.5rem' }}>
                          {results.disease_info.symptoms.map((symptom, index) => (
                            <li key={index} style={{ marginBottom: '0.25rem' }}>{symptom}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {results.disease_info.causes && (
                      <div style={{ marginBottom: '1rem' }}>
                        <strong>Causes:</strong> {results.disease_info.causes}
                      </div>
                    )}
                    {results.disease_info.treatment && (
                      <div style={{ marginBottom: '1rem' }}>
                        <strong>Treatment:</strong> {results.disease_info.treatment}
                      </div>
                    )}
                    {results.disease_info.prevention && (
                      <div>
                        <strong>Prevention:</strong> {results.disease_info.prevention}
                      </div>
                    )}
                  </ResultContent>
                </ResultCard>
              )}
            </div>
          )}
        </ResultsSection>
      </ContentGrid>
    </DetectionContainer>
  );
}

export default DiseaseDetection;
