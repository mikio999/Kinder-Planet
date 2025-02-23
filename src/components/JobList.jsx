import { useEffect, useState } from "react";
import { db, collection, getDocs } from "../firebase";
import {
  Card,
  CardContent,
  Container,
  Typography,
  Link,
  Box,
  Button,
} from "@mui/material";
import useMediaQuery from "@mui/material/useMediaQuery";

const JobList = () => {
  const [jobs, setJobs] = useState([]);
  const [visibleCount, setVisibleCount] = useState(10);
  const isMobile = useMediaQuery("(max-width: 768px)");

  useEffect(() => {
    const fetchJobs = async () => {
      // ✅ CAU Jobs 가져오기
      const cauQuerySnapshot = await getDocs(collection(db, "cau_jobs"));
      const cauJobs = cauQuerySnapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
      }));

      // ✅ Gogane Jobs 가져오기
      const goganeQuerySnapshot = await getDocs(collection(db, "gogane_jobs"));
      const goganeJobs = goganeQuerySnapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
      }));

      // ✅ Seoul Jobs 가져오기
      const seoulQuerySnapshot = await getDocs(collection(db, "seoul_jobs"));
      const seoulJobs = seoulQuerySnapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
      }));

      // ✅ 모든 공고를 날짜순 정렬 후 상태 업데이트
      const combinedJobs = [...cauJobs, ...goganeJobs, ...seoulJobs].sort(
        (a, b) => b.date.localeCompare(a.date)
      );

      setJobs(combinedJobs);
    };

    fetchJobs();
  }, []);

  const loadMore = () => {
    setVisibleCount((prevCount) => prevCount + 10);
  };

  return (
    <Container>
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: isMobile ? "1fr" : "repeat(2, 1fr)",
          gap: 2,
          width: "100%",
          paddingBottom: 4,
        }}
      >
        {jobs.slice(0, visibleCount).map((job) => (
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
                minHeight: "180px",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                transition: "0.3s",
                cursor: "pointer",
                "&:hover": { boxShadow: 3 },
                wordBreak: "break-word",
                overflowWrap: "break-word",
              }}
            >
              <CardContent sx={{ textAlign: "center" }}>
                <Typography
                  variant="h6"
                  sx={{ fontWeight: "bold", wordBreak: "keep-all" }}
                >
                  {job.title}
                </Typography>
                <Typography color="textSecondary">📅 {job.date}</Typography>
              </CardContent>
            </Card>
          </Link>
        ))}

        {/* 더보기 버튼 */}
      </Box>
      {visibleCount < jobs.length && (
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            width: "100%",
            marginTop: 3,
          }}
        >
          <Button variant="contained" onClick={loadMore}>
            공고 더보기
          </Button>
        </Box>
      )}
    </Container>
  );
};

export default JobList;
