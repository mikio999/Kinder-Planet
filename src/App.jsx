import { useState, useMemo } from "react";
import JobList from "./components/JobList";
import Footer from "./components/Footer.jsx";
import {
  Container,
  Typography,
  CssBaseline,
  ThemeProvider,
  createTheme,
  Switch,
} from "@mui/material";
import useMediaQuery from "@mui/material/useMediaQuery";

function App() {
  const prefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)");
  const [darkMode, setDarkMode] = useState(prefersDarkMode);

  const theme = useMemo(
    () =>
      createTheme({
        typography: {
          fontFamily:
            '"42dot Sans", "Roboto", "Helvetica", "Arial", sans-serif',
        },
        palette: {
          mode: darkMode ? "dark" : "light",
          primary: {
            main: darkMode ? "#90caf9" : "#1976d2",
          },
          background: {
            default: darkMode ? "#121212" : "rgb(241, 245, 249)",
            paper: darkMode ? "#1e1e1e" : "#ffffff",
          },
          text: {
            primary: darkMode ? "#ffffff" : "#000000",
          },
        },
      }),
    [darkMode]
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container
        maxWidth="md"
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          minHeight: "100vh",
          textAlign: "center",
        }}
      >
        <Container
          sx={{
            display: "flex",
            padding: "2rem",
            justifyContent: "center",
          }}
        >
          {" "}
          <Typography variant="h4" sx={{ fontFamily: '"Jua", sans-serif' }}>
            👶 유치원 공고 🚌
          </Typography>
          <Switch checked={darkMode} onChange={() => setDarkMode(!darkMode)} />
        </Container>
        <JobList />
      </Container>
      <Footer /> {/* Footer 추가 */}
    </ThemeProvider>
  );
}

export default App;
