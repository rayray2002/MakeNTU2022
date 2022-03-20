import {Alert,AlertTitle,Button, makeStyles, Typography } from "@mui/material";
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



const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
`;



const Stats = () =>{
    const [over, setOver] = useState(true)
    const makeAPICall = async () => {
        try {
          const response = await fetch('http://10.20.2.194:8000/out.json', {mode:'cors'});
          const Statdata = await response.json();
          //overlimit = Statdata.overlimit;
          console.log(Statdata.ac_electricity)
          return Statdata
        }
        catch (e) {
          console.log(e)
        }
      }
      useEffect(() => {
        let p = makeAPICall();
        p.then(response=>setOver(response.overlimit)); 
        console.log(typeof over);
      }, [over])
    
    const [datanum, setData] = useState([1,2,30])
    let series = [{
        data: datanum
    }];
    let test;
    let head;
    if(over === "true"){head = <Alert severity="warning" action={<Button color="inherit" size="small">x</Button>}>
    <AlertTitle>Warning</AlertTitle>
    您的B電器使用...... — <strong>!</strong>
    </Alert>}
    else{head = <p>test</p>}
    return(
        <Wrapper>
            {head}
            <Stack spacing={2}>
                <Typography text-align='center' variant='h4'>今日使用報告</Typography>
                <Typography text-align='center' variant='h5'>若維持.......</Typography>
                <Typography text-align='center' variant='h5'>{test}</Typography>
                <meta http-equiv='refresh' content='30'/>
                <Button variant='outlined' size='large'>Refresh Data</Button>
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