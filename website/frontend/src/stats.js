import {Alert,AlertTitle,Button,Collapse,Divider,Typography } from "@mui/material";
import styled from 'styled-components'
import CoolInput from "./CoolInput";
import Box from '@mui/material/Box';
import { ContactSupportOutlined, IosShare } from "@mui/icons-material";
import { Stack } from "@mui/material"; 
import {
    // main component
    Chart,
    // graphs
    Bars, Cloud, Dots, Labels, Lines, Pies, RadialLines, Ticks, Title,
    // wrappers
    Layer, Animate, Transform, Handlers,
    // helpers
    helpers, DropShadow, Gradient
  } from 'rumble-charts';
import { useEffect, useState } from "react";
//import { getalldata } from "./axios";
import { createTheme, ThemeProvider} from '@mui/material/styles';
import cwtexfangsong from './fonts/cwtexfangsong-zhonly.ttf'

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
`;

const theme = createTheme({
    typography: {
      fontFamily: [
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
        'Roboto',
        '"Helvetica Neue"',
        'Arial',
        'sans-serif',
        '"Apple Color Emoji"',
        '"Segoe UI Emoji"',
        '"Segoe UI Symbol"',
      ].join(','),
    },
  });

const Stats = () =>{
    const [open, setOpen] = useState(true);
    const [ac_electricity,setAC_electricity] = useState(0);
    const [ac_usage,setAC_usage] = useState(0);
    const [solar_electricity,setSolar_electricity] = useState(0);
    const [solar_usage,setSolar_usage] = useState(0);
    const [predfee,setPredfee] = useState(0);
    const [aclimit,setAClimit] = useState(true);
    const [total_electricity,setTotal_electricity] = useState(0);
    const [total_usage,setTotal_usage] = useState(0);

    //const [over, setOver] = useState(true)
    const makeAPICall = async () => {
        try {
          const response = await fetch('http://10.20.2.194:8000/out.json', {mode:'cors'});
          const Statdata = await response.json();
          //overlimit = Statdata.overlimit;
          //console.log(Statdata.aclimit)
          return Statdata
        }
        catch (e) {
          console.log(e)
        }
      }
      useEffect(() => {
        let p = makeAPICall();
        p.then(response=>setAC_electricity(response.ac_electricity)); 
        p.then(response=>setAC_usage(response.ac_usage));
        p.then(response=>setSolar_electricity(response.solar_electricity));
        p.then(response=>setSolar_usage(response.solar_usage));
        p.then(response=>setPredfee(response.predfee));
        p.then(response=> setAClimit(response.aclimit));
        p.then(response=>setTotal_electricity(response.total_electricity));
        p.then(response=>setTotal_usage(response.total_usage));
      }, [])
    let caution;
    if(String(aclimit) === 'true'){
        caution = 
            <Box sx={{ width: '100%' }}>
                <Collapse in={open}>
                    <Alert severity="warning" action={<Button color="inherit" size="small" 
                    onClick={() => {setOpen(false)}}>確認並關閉</Button>}>
                        <AlertTitle>Warning</AlertTitle>
                        您已達日用電上限 <strong>!</strong>
                    </Alert>
                </Collapse>
            </Box>
    }
    else{
        caution = <></>
    }
    return(
        <Wrapper>
            <Stack spacing={2}>
                {caution}
                <ThemeProvider theme={theme}>
                    <Typography text-align='center' variant='h4' fontFamily='sans-serif'>今日使用報告</Typography>
                </ThemeProvider>
                <Divider></Divider>
                <Typography text-align='center' variant='h5'>預測電費 : {predfee} 元</Typography>
                <Divider></Divider>
                <Typography text-align='center' variant='h7'>冷氣用電量 : {ac_electricity}</Typography>
                <Divider></Divider>
                <Typography text-align='center' variant='h7'>冷氣用電功率 : {ac_usage}</Typography>
                <Divider></Divider>
                <Typography text-align='center' variant='h7'>日用電上限 : {String(aclimit)}</Typography>
                <Divider></Divider>
                <Typography text-align='center' variant='h7'>太陽能板發電量: {solar_electricity}</Typography>
                <Divider></Divider>
                <Typography text-align='center' variant='h7'>太陽能板發電功率 : {solar_usage}</Typography>
                <Divider></Divider>
                <Typography text-align='center' variant='h7'>總消耗電量 : {total_electricity}</Typography>
                <Divider></Divider>
                <Typography text-align='center' variant='h7'>總消耗功率 : {total_usage}</Typography>
                <meta http-equiv='refresh' content='10'/>
                <Divider></Divider>
                <Box sx={{width: 800,height: 600 ,border:'1px dashed grey'}}>
                    <Wrapper>
                        <br/>
                        <Typography variant='h5'>太陽能板發電功率</Typography>
                        <img src='http://10.20.2.194:8000/solar_electricity.png'/>
                    </Wrapper>
                </Box>
                <Box sx={{width: 800,height: 600 ,border:'1px dashed grey'}}>
                    <Wrapper>
                        <br/>
                        <Typography variant='h5'>冷氣用電功率</Typography>
                        <img src='http://10.20.2.194:8000/electricity.png'/>
                    </Wrapper>
                </Box>
                <Box sx={{width: 800,height: 600 ,border:'1px dashed grey'}}>
                    <Wrapper>
                        <br/>
                        <Typography variant='h5'>總消耗功率</Typography>
                        <img src='http://10.20.2.194:8000/ac_electricity.png'/>
                    </Wrapper>
                </Box>

                <Box sx={{width: 800,height: 600 ,border:'1px dashed grey'}}>
                    <Wrapper>
                        <br/>
                        <Typography variant='h5'>太陽能發電量</Typography>
                        <img src='http://10.20.2.194:8000/solar_usage.png'/>
                    </Wrapper>
                </Box>
                <Box sx={{width: 800,height: 600 ,border:'1px dashed grey'}}>
                    <Wrapper>
                        <br/>
                        <Typography variant='h5'>總用電量</Typography>
                        <img src='http://10.20.2.194:8000/total_usage.png'/>
                    </Wrapper>
                </Box>
            </Stack>
        </Wrapper>    
    )
}
export default Stats;