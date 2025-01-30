import { Box, Typography, Link, Container } from "@mui/material";
import { GitHub, LinkedIn } from "@mui/icons-material";
import ArticleIcon from "@mui/icons-material/Article";

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        mt: 4,
        width: "100%",
        backgroundColor: "rgba(0, 0, 0, 0.8)",
        color: "white",
        textAlign: "center",
      }}
    >
      <Container>
        <Typography
          variant="body1"
          sx={{ fontSize: "0.75rem", textAlign: "left" }}
          gutterBottom
        >
          본 사이트는 중앙대학교 유아교육과 (예비) 졸업생이 만든 사이트입니다.
          <br /> 본 공고는 중앙대학교 유아교육과 취업게시판, 고가네에서
          스크래이핑했습니다.
          <br /> 모두 취뽀하세요 동문님들 🙇‍♀️
        </Typography>

        <Box sx={{ display: "flex", justifyContent: "center", gap: 2, mt: 1 }}>
          <Link
            href="https://github.com/mikio999"
            target="_blank"
            color="inherit"
          >
            <GitHub sx={{ fontSize: 28 }} />
          </Link>
          <Link
            href="https://velog.io/@mikio/posts"
            target="_blank"
            color="inherit"
          >
            <ArticleIcon sx={{ fontSize: 28 }} />
          </Link>
          <Link
            href="https://www.linkedin.com/in/%EB%AF%BC%EA%B2%BD-%EA%B3%BD-02744a302/"
            target="_blank"
            color="inherit"
          >
            <LinkedIn sx={{ fontSize: 28 }} />
          </Link>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;
