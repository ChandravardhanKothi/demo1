import React from 'react';
import { NavLink } from 'react-router-dom';
import styled from 'styled-components';
import { 
  Home, 
  Camera, 
  Cloud, 
  TrendingUp, 
  FileText, 
  User,
  X
} from 'lucide-react';

const SidebarContainer = styled.aside`
  position: fixed;
  top: 64px;
  left: 0;
  width: 250px;
  height: calc(100vh - 64px);
  background: white;
  border-right: 1px solid #e5e7eb;
  transform: ${props => props.isOpen ? 'translateX(0)' : 'translateX(-100%)'};
  transition: transform 0.3s ease;
  z-index: 999;
  overflow-y: auto;
  
  @media (max-width: 768px) {
    width: 100%;
    z-index: 1001;
  }
`;

const SidebarHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  
  @media (min-width: 769px) {
    display: none;
  }
`;

const CloseButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  border-radius: 6px;
  cursor: pointer;
  color: #6b7280;
  
  &:hover {
    background-color: #f3f4f6;
    color: #374151;
  }
`;

const NavList = styled.nav`
  padding: 1rem 0;
`;

const NavItem = styled(NavLink)`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  color: #6b7280;
  text-decoration: none;
  transition: all 0.2s ease;
  border-right: 3px solid transparent;
  
  &:hover {
    background-color: #f9fafb;
    color: #374151;
  }
  
  &.active {
    background-color: #eff6ff;
    color: #3b82f6;
    border-right-color: #3b82f6;
    font-weight: 600;
  }
`;

const NavIcon = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
`;

const NavText = styled.span`
  font-size: 0.875rem;
  font-weight: 500;
`;

const SidebarSection = styled.div`
  margin-bottom: 2rem;
`;

const SectionTitle = styled.div`
  padding: 0.5rem 1.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const UserInfo = styled.div`
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  margin-top: auto;
`;

const UserDetails = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const UserAvatar = styled.div`
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
`;

const UserText = styled.div`
  flex: 1;
`;

const UserName = styled.div`
  font-weight: 600;
  color: #1f2937;
  font-size: 0.875rem;
`;

const UserLocation = styled.div`
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.125rem;
`;

const StatusIndicator = styled.div`
  width: 8px;
  height: 8px;
  background-color: #10b981;
  border-radius: 50%;
  margin-left: auto;
`;

const menuItems = [
  {
    title: 'Dashboard',
    path: '/dashboard',
    icon: Home,
    section: 'main'
  },
  {
    title: 'Disease Detection',
    path: '/disease-detection',
    icon: Camera,
    section: 'main'
  },
  {
    title: 'Weather',
    path: '/weather',
    icon: Cloud,
    section: 'main'
  },
  {
    title: 'Market Prices',
    path: '/market',
    icon: TrendingUp,
    section: 'main'
  },
  {
    title: 'Advisories',
    path: '/advisories',
    icon: FileText,
    section: 'main'
  },
  {
    title: 'Profile',
    path: '/profile',
    icon: User,
    section: 'account'
  }
];

function Sidebar({ isOpen, onClose }) {
  const mainItems = menuItems.filter(item => item.section === 'main');
  const accountItems = menuItems.filter(item => item.section === 'account');

  return (
    <SidebarContainer isOpen={isOpen}>
      <SidebarHeader>
        <span style={{ fontWeight: '600', color: '#1f2937' }}>Menu</span>
        <CloseButton onClick={onClose}>
          <X size={20} />
        </CloseButton>
      </SidebarHeader>
      
      <NavList>
        <SidebarSection>
          {mainItems.map((item) => (
            <NavItem key={item.path} to={item.path} onClick={onClose}>
              <NavIcon>
                <item.icon size={20} />
              </NavIcon>
              <NavText>{item.title}</NavText>
            </NavItem>
          ))}
        </SidebarSection>
        
        <SidebarSection>
          <SectionTitle>Account</SectionTitle>
          {accountItems.map((item) => (
            <NavItem key={item.path} to={item.path} onClick={onClose}>
              <NavIcon>
                <item.icon size={20} />
              </NavIcon>
              <NavText>{item.title}</NavText>
            </NavItem>
          ))}
        </SidebarSection>
      </NavList>
      
      <UserInfo>
        <UserDetails>
          <UserAvatar>JD</UserAvatar>
          <UserText>
            <UserName>John Doe</UserName>
            <UserLocation>Hyderabad, Telangana</UserLocation>
          </UserText>
          <StatusIndicator />
        </UserDetails>
      </UserInfo>
    </SidebarContainer>
  );
}

export default Sidebar;
