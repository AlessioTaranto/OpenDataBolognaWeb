import React, { useState } from "react";
import { TextField, PrimaryButton, Stack, MessageBar, MessageBarType, Spinner, SpinnerSize } from "@fluentui/react";
import { ThemeProvider, DefaultButton } from "@fluentui/react";
import { myTheme } from "./theme";
import axios from "axios";

// Define a simple card component using native Fluent UI components
const Card = ({ children, title }) => (
  <div style={{ border: '1px solid #ccc', padding: 20, borderRadius: 4, marginTop: 20 }}>
    <h3>{title}</h3>
    {children}
  </div>
);

function App() {
  const [date, setDate] = useState("");
  const [precipitationData, setPrecipitationData] = useState(null);
  const [dataset, setDataset] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchPrecipitation = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`http://localhost:8000/precipitation?date=${date}`);
      setPrecipitationData(response.data);
    } catch (err) {
      setError("Failed to fetch precipitation data: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchDataset = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`http://localhost:8000/dataset`);
      setDataset(response.data);
    } catch (err) {
      setError("Failed to fetch dataset: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={myTheme}>
      <div style={{ padding: 20 }}>
        <h1 style={{ textAlign: "center", color: myTheme.palette.themePrimary }}>Bologna Precipitation Data</h1>

        <Stack tokens={{ childrenGap: 15 }} styles={{ root: { maxWidth: 600, margin: '0 auto' } }}>
          <TextField
            label="Enter Date (YYYY-MM-DD)"
            value={date}
            onChange={(e, newValue) => setDate(newValue)}
            placeholder="YYYY-MM-DD"
          />

          <Stack horizontal tokens={{ childrenGap: 10 }}>
            <PrimaryButton text="Fetch Weekly Precipitation" onClick={fetchPrecipitation} />
            <PrimaryButton text="Fetch Dataset" onClick={fetchDataset} />
          </Stack>

          {loading && <Spinner size={SpinnerSize.large} label="Loading data..." />}

          {error && (
            <MessageBar messageBarType={MessageBarType.error} isMultiline={false} dismissButtonAriaLabel="Close">
              {error}
            </MessageBar>
          )}

          {/* Display precipitation data */}
          {precipitationData && (
            <Card title="Weekly Precipitation Data">
              <ul>
                {precipitationData.results.map((record, index) => (
                  <li key={index}>
                    {record.date} - {record.avg_184_d} mm ({record.stagione})
                  </li>
                ))}
              </ul>
            </Card>
          )}

          {/* Display dataset */}
          {dataset && (
            <Card title="Complete Dataset">
              <pre>{JSON.stringify(dataset, null, 2)}</pre>
            </Card>
          )}
        </Stack>
      </div>
    </ThemeProvider>
  );
}

export default App;
