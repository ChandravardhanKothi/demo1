import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { 
  TrendingUp, 
  Cloud, 
  AlertTriangle, 
  CheckCircle,
  Camera,
  MapPin,
  Calendar
} from 'lucide-react';
import toast from 'react-hot-toast';

// Components
import WeatherCard from '../components/WeatherCard';
import MarketCard from '../components/MarketCard';
import RecentDetection from '../components/RecentDetection';
import AdvisoryCard from '../components/AdvisoryCard';

const DashboardContainer = styled.div`
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

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const StatCard = styled.div`
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
`;

const StatHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
`;

const StatTitle = styled.h3`
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const StatIcon = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: ${props => props.bgColor || '#f3f4f6'};
  color: ${props => props.color || '#6b7280'};
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
`;

const StatChange = styled.div`
  font-size: 0.875rem;
  color: ${props => props.positive ? '#10b981' : '#ef4444'};
  display: flex;
  align-items: center;
  gap: 0.25rem;
`;

const ContentGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  
  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
`;

const MainContent = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const SidebarContent = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const QuickActions = styled.div`
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
`;

const QuickActionsTitle = styled.h3`
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
`;

const ActionButton = styled.button`
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 0.5rem;
  
  &:hover {
    background-color: #f9fafb;
    border-color: #d1d5db;
  }
  
  &:last-child {
    margin-bottom: 0;
  }
`;

function Dashboard() {
  const [stats, setStats] = useState({
    totalDetections: 0,
    healthyCrops: 0,
    diseasedCrops: 0,
    activeAdvisories: 0
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading data
    const timer = setTimeout(() => {
      setStats({
        totalDetections: 24,
        healthyCrops: 18,
        diseasedCrops: 6,
        activeAdvisories: 3
      });
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const handleQuickAction = (action) => {
    toast.success(`${action} feature coming soon!`);
  };

  if (loading) {
    return (
      <DashboardContainer>
        <div className="loading">
          <div className="spinner"></div>
        </div>
      </DashboardContainer>
    );
  }

  return (
    <DashboardContainer>
      <Header>
        <Title>Dashboard</Title>
        <Subtitle>Welcome back! Here's what's happening with your crops today.</Subtitle>
      </Header>

      <StatsGrid>
        <StatCard>
          <StatHeader>
            <StatTitle>Total Detections</StatTitle>
            <StatIcon bgColor="#eff6ff" color="#3b82f6">
              <Camera size={20} />
            </StatIcon>
          </StatHeader>
          <StatValue>{stats.totalDetections}</StatValue>
          <StatChange positive>
            <TrendingUp size={16} />
            +12% from last month
          </StatChange>
        </StatCard>

        <StatCard>
          <StatHeader>
            <StatTitle>Healthy Crops</StatTitle>
            <StatIcon bgColor="#ecfdf5" color="#10b981">
              <CheckCircle size={20} />
            </StatIcon>
          </StatHeader>
          <StatValue>{stats.healthyCrops}</StatValue>
          <StatChange positive>
            <TrendingUp size={16} />
            +8% from last week
          </StatChange>
        </StatCard>

        <StatCard>
          <StatHeader>
            <StatTitle>Diseased Crops</StatTitle>
            <StatIcon bgColor="#fef2f2" color="#ef4444">
              <AlertTriangle size={20} />
            </StatIcon>
          </StatHeader>
          <StatValue>{stats.diseasedCrops}</StatValue>
          <StatChange positive={false}>
            <TrendingUp size={16} />
            -3% from last week
          </StatChange>
        </StatCard>

        <StatCard>
          <StatHeader>
            <StatTitle>Active Advisories</StatTitle>
            <StatIcon bgColor="#fef3c7" color="#f59e0b">
              <AlertTriangle size={20} />
            </StatIcon>
          </StatHeader>
          <StatValue>{stats.activeAdvisories}</StatValue>
          <StatChange positive>
            <TrendingUp size={16} />
            2 new today
          </StatChange>
        </StatCard>
      </StatsGrid>

      <ContentGrid>
        <MainContent>
          <WeatherCard />
          <RecentDetection />
        </MainContent>

        <SidebarContent>
          <MarketCard />
          <QuickActions>
            <QuickActionsTitle>Quick Actions</QuickActionsTitle>
            <ActionButton onClick={() => handleQuickAction('Upload Crop Image')}>
              <Camera size={20} />
              Upload Crop Image
            </ActionButton>
            <ActionButton onClick={() => handleQuickAction('Check Weather')}>
              <Cloud size={20} />
              Check Weather
            </ActionButton>
            <ActionButton onClick={() => handleQuickAction('View Market Prices')}>
              <TrendingUp size={20} />
              View Market Prices
            </ActionButton>
            <ActionButton onClick={() => handleQuickAction('Get Advisory')}>
              <AlertTriangle size={20} />
              Get Advisory
            </ActionButton>
          </QuickActions>
          
          <AdvisoryCard />
        </SidebarContent>
      </ContentGrid>
    </DashboardContainer>
  );
}

export default Dashboard;
