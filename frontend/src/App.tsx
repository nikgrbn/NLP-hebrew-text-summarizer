import { CacheProvider } from "@emotion/react";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import rtlPlugin from "stylis-plugin-rtl";
import { prefixer } from "stylis";
import createCache from "@emotion/cache";
import event from "./strings";
import React, {
  PropsWithChildren,
  useEffect,
  useLayoutEffect,
  useState,
} from "react";
import "./App.css";
import Grid from "@mui/material/Grid";
import { Typography } from "@mui/material";

const isRtl = true; // this constant eventually should end up in a context provider

// Create rtl cache
const cacheRtl = createCache({
  key: "muirtl",
  stylisPlugins: [prefixer, rtlPlugin],
});

function RTL({ children }: PropsWithChildren<{}>) {
  if (isRtl) {
    return <CacheProvider value={cacheRtl}>{children}</CacheProvider>;
  } else {
    return <>{children}</>;
  }
}

function App() {
  useLayoutEffect(() => {
    document.body.setAttribute("dir", isRtl ? "rtl" : "ltr");
  }, [isRtl]);

  const [summary, setSummary] = useState("");
  const [text, setText] = useState("");
  const [textError, setTextError] = useState(false);


  const init: RequestInit = {
    mode: "cors",
    method: "POST",
    headers: {
      "Content-Type": "text/plain",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "*",
    },
    body: JSON.stringify(text),
  };

  const handleClick = () => {
    setTextError(false)

    if(text === '')
    {
      setTextError(true)
    }
    else{
      fetch("http://127.0.0.1:5000/summary", init)
      .then((res) => res.json())
      .then((data) => {
        setSummary(data.payload);
        console.log(summary);
      });
    }
    
  };

  return (
    <div className="App">
      <Grid container rowSpacing={2} direction="row">
        <Grid item xs={0.5} md={0.5}></Grid>
        <Grid item xs={11.5} md={11.5}>
          <Grid
            container
            justifyContent="flex-start"
            alignItems="flex-start"
            direction="column"
            rowSpacing={2}
          >
            <RTL>
              <Grid item xs={12} md={12}>
                <Typography variant="h1">{event.Title}</Typography>
              </Grid>

              <Grid item xs={12} md={12}>
                <TextField
                  id="outlined-multiline-static"
                  label={event.Text}
                  multiline
                  rows={20}
                  value={text}
                  onChange={(event) => {
                    setText(event.target.value);
                  }}
                  defaultValue={event.UserText}
                  error={textError}
                  style={{ width: "700%" }}
                />
              </Grid>
              <Grid item xs={12} md={12}>
                <Button variant="contained" onClick={handleClick}>
                  {event.Submit}
                </Button>
              </Grid>
              <Grid item xs={12} md={12}>
                <TextField
                  id="filled-disabled"
                  label={event.Summary}
                  defaultValue={event.HereSummary}
                  variant="filled"
                  value={summary}
                  style={{ width: "300%" }}
                  rows={10}
                  sx={{ input: { color: 'red' } }}
                  disabled
                  multiline
                />
              </Grid>
              <Grid item xs={12} md={12} />
            </RTL>
          </Grid>
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
