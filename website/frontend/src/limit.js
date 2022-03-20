import {Alert,AlertTitle,Button,InputAdornment, OutlinedInput, Typography } from "@mui/material";
import styled from 'styled-components'
import CoolInput from "./CoolInput";
import { TextField } from "@mui/material";
import Box from '@mui/material/Box';
import { Stack } from "@mui/material";
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import { useState } from "react";
import Caution from "./caution";
//import {writeJsonFile} from 'write-json-file';
import * as fs from 'fs'
const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;
const Col_wrapper = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center; 
`
const Limit = () =>{
    //const [lim,setLim] = useState(0);
    const [bill,setBill] = useState(0);
    const handleBill = ()=>{
        let inttime = parseInt(values.time)
        let intlim  = parseInt(values.lim)
        setBill(inttime*intlim*0+10);
        //setLim(1);
    }
    const [values, setValues] = useState({
        time: '',
        lim: ''
      });
    const handleChange = (prop) => (event) => {
    setValues({ ...values, [prop]: event.target.value });
    };

    const handleLimit = ()=>{
        const cooldata = {
            limit:0
        }
        const jsonString = JSON.stringify(cooldata)
        fs.writeFile('../../testser/limit.json', jsonString, err => {
            if (err) {
                console.log('Error writing file', err)
            } else {
                console.log('Successfully wrote file')
            }
        })
    }
    
    return(
        <>
            <Wrapper>
                <Box component="span" sx={{ p: 20, border: '1px dashed grey' }}>
                    <Stack spacing={2}>
                        <Col_wrapper>
                            <LightbulbIcon fontSize="large"/>
                            <Typography variant='h2'>Upper limit of electricity</Typography>
                        </Col_wrapper>
                        <TextField defaultValue='10' label="Time limit" variant="standard" value={values.time} onChange={handleChange('time')}
                         endAdornment={<InputAdornment position="end">hr</InputAdornment>} />
                        <TextField defaultValue='10' label="Time limit" variant="standard" value={values.lim} onChange={handleChange('lim')} 
                        endAdornment={<InputAdornment position="end">hr</InputAdornment>} />
                        <Button variant="contained" color="success" onClick={handleBill}>Apply</Button>
                        <Typography variant='h3'>估計用電上限理想值 = {bill}</Typography>
                    </Stack>
                </Box>
                <br/>
                <Alert severity="warning" action={<Button color="inherit" size="small">x</Button>}>
                    <AlertTitle>Warning</AlertTitle>
                    您的B電器使用...... — <strong>!</strong>
                </Alert>
            </Wrapper>    
        </>
    )
}
export default Limit;