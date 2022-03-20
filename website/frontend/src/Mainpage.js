import Block from './Block';
import { useState } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import Navbar from './navbar';
import Stats from './stats'
import Limit from './limit';
import { Paper } from '@mui/material';
import './index.css'

const MainPage = () =>{
    const [mode, SetMode] = useState('stats');
    return (
        <>
        <div className="head">
            <Navbar mode ={mode} setMode={SetMode}/>
        </div>
        <br/>
        <div>
            <Paper style={{ background: '#FCFAF2' }} elevation = {1}>
                {mode === 'home'? (<Button>Home</Button>): mode === 'stats' ?(<Stats/>) :<Limit/>}
            </Paper>
        </div>
        </>
  );
}

export default MainPage;
