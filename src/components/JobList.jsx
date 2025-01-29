import { useEffect, useState } from "react";
import { db, collection, getDocs } from "../firebase";
import { Card, CardContent, Typography, Link, Box } from "@mui/material";
import useMediaQuery from "@mui/material/useMediaQuery";

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const isMobile = useMediaQuery("(max-width: 768px)"); // 모바일 반응형 감지

  useEffect(() => {
    const fetchJobs = async () => {
      const querySnapshot = await getDocs(collection(db, "cau_jobs"));
      const jobData = querySnapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
      }));
      setJobs(jobData);
    };

    fetchJobs();
  }, []);

  return (
    <Box
      sx={{
        display: "grid",
        gridTemplateColumns: isMobile ? "1fr" : "repeat(2, 1fr)", // 모바일 1열, PC 2열
        gap: 2,
        width: "100%",
      }}
    >
      {jobs.map((job) => (
        <Link
          key={job.id}
          href={job.link}
          target="_blank"
          rel="noopener noreferrer"
          sx={{
            textDecoration: "none",
            color: "inherit",
          }}
        >
          <Card
            variant="outlined"
            sx={{
              height: "180px", // 카드 높이 고정
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              transition: "0.3s",
              cursor: "pointer",
              "&:hover": {
                boxShadow: 3,
              },
              wordBreak: "keep-all",
              overflowWrap: "break-word",
            }}
          >
            <CardContent sx={{ textAlign: "center" }}>
              <Typography variant="h6" sx={{ fontWeight: "bold" }}>
                {job.title}
              </Typography>
              <Typography color="textSecondary">📅 {job.date}</Typography>
            </CardContent>
          </Card>
        </Link>
      ))}
    </Box>
  );
};

export default JobList;
