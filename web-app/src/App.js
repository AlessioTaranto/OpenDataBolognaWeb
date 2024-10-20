import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Box,
  Card,
  CardContent,
  Container,
  Grid,
  Paper,
  Tab,
  Tabs,
  TextField,
  ThemeProvider,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  createTheme,
} from '@mui/material';
import { styled } from '@mui/system';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
} from '@mui/lab';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer 
} from 'recharts';
import { 
  WbSunny, 
  Cloud, 
  Opacity, 
  CalendarToday, 
  Storage 
} from '@mui/icons-material';

// Create a custom theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

// Styled components
const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: theme.shadows[8],
  },
}));

const WeatherDashboard = () => {
  const [date, setDate] = useState(new Date("2023-01-01").toISOString().split('T')[0]);
  const [precipitationData, setPrecipitationData] = useState(null);
  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tabValue, setTabValue] = useState(0);

  const fetchPrecipitation = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8000/precipitation?date=${date}`);
      if (!response.ok) throw new Error('Failed to fetch precipitation data');
      const data = await response.json();
      setPrecipitationData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchDataset = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/dataset');
      if (!response.ok) throw new Error('Failed to fetch dataset');
      const data = await response.json();
      setDataset(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPrecipitation();
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const getWeatherIcon = (precipitation) => {
    if (precipitation > 10) return <Opacity />;
    if (precipitation > 5) return <Cloud />;
    return <WbSunny />;
  };

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static" color="primary">
          <Typography variant="h4" component="div" sx={{ flexGrow: 1, p: 2, textAlign: 'center' }}>
            Weather Dashboard
          </Typography>
        </AppBar>
        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Grid container spacing={3}>
            {/* Controls */}
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 2 }}>
                <Grid container spacing={2} alignItems="center">
                  <Grid item>
                    <TextField
                      type="date"
                      value={date}
                      onChange={(e) => setDate(e.target.value)}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={fetchPrecipitation}
                      startIcon={<Opacity />}
                    >
                      Fetch Precipitation
                    </Button>
                  </Grid>
                  <Grid item>
                    <Button
                      variant="outlined"
                      color="secondary"
                      onClick={fetchDataset}
                      startIcon={<Storage />}
                    >
                      Fetch Dataset
                    </Button>
                  </Grid>
                </Grid>
              </Paper>
            </Grid>

            {/* Loading and Error states */}
            {loading && (
              <Grid item xs={12}>
                <Paper elevation={3} sx={{ p: 2, textAlign: 'center' }}>
                  <Typography>Loading...</Typography>
                </Paper>
              </Grid>
            )}
            {error && (
              <Grid item xs={12}>
                <Paper elevation={3} sx={{ p: 2, bgcolor: 'error.main', color: 'error.contrastText' }}>
                  <Typography>Error: {error}</Typography>
                </Paper>
              </Grid>
            )}

            {/* Precipitation Data */}
            {precipitationData && (
              <Grid item xs={12}>
                <StyledCard>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      <CalendarToday sx={{ mr: 1 }} />
                      Weekly Precipitation Data
                    </Typography>
                    <Tabs value={tabValue} onChange={handleTabChange} centered>
                      <Tab label="Chart" />
                      <Tab label="Table" />
                      <Tab label="Timeline" />
                    </Tabs>
                    <Box sx={{ mt: 2 }}>
                      {tabValue === 0 && (
                        <Box sx={{ height: 300 }}>
                          <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={precipitationData.results}>
                              <CartesianGrid strokeDasharray="3 3" />
                              <XAxis dataKey="date" />
                              <YAxis />
                              <Tooltip />
                              <Line 
                                type="monotone" 
                                dataKey="avg_184_d" 
                                stroke="#8884d8" 
                                activeDot={{ r: 8 }} 
                              />
                            </LineChart>
                          </ResponsiveContainer>
                        </Box>
                      )}
                      {tabValue === 1 && (
                        <TableContainer component={Paper}>
                          <Table>
                            <TableHead>
                              <TableRow>
                                <TableCell>Date</TableCell>
                                <TableCell>Precipitation</TableCell>
                                <TableCell>Season</TableCell>
                                <TableCell>Weather</TableCell>
                              </TableRow>
                            </TableHead>
                            <TableBody>
                              {precipitationData.results.map((record, index) => (
                                <TableRow key={index}>
                                  <TableCell>{record.date}</TableCell>
                                  <TableCell>{record.avg_184_d} mm</TableCell>
                                  <TableCell>{record.stagione}</TableCell>
                                  <TableCell>{getWeatherIcon(record.avg_184_d)}</TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </TableContainer>
                      )}
                      {tabValue === 2 && (
                        <Timeline position="alternate">
                          {precipitationData.results.map((record, index) => (
                            <TimelineItem key={index}>
                              <TimelineSeparator>
                                <TimelineDot color={record.avg_184_d > 5 ? "primary" : "secondary"}>
                                  {getWeatherIcon(record.avg_184_d)}
                                </TimelineDot>
                                {index < precipitationData.results.length - 1 && <TimelineConnector />}
                              </TimelineSeparator>
                              <TimelineContent>
                                <Typography variant="h6" component="span">
                                  {record.date}
                                </Typography>
                                <Typography>{record.avg_184_d} mm</Typography>
                                <Typography variant="body2" color="text.secondary">
                                  {record.stagione}
                                </Typography>
                              </TimelineContent>
                            </TimelineItem>
                          ))}
                        </Timeline>
                      )}
                    </Box>
                  </CardContent>
                </StyledCard>
              </Grid>
            )}

            {/* Dataset */}
            {dataset && (
              <Grid item xs={12}>
                <StyledCard>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      <Storage sx={{ mr: 1 }} />
                      Complete Dataset
                    </Typography>
                    <Paper elevation={3} sx={{ p: 2, maxHeight: 400, overflow: 'auto' }}>
                      <pre>{JSON.stringify(dataset, null, 2)}</pre>
                    </Paper>
                  </CardContent>
                </StyledCard>
              </Grid>
            )}
          </Grid>
        </Container>
      </Box>
    </ThemeProvider>
  );
};

export default WeatherDashboard;