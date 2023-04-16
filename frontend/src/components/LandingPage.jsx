import React from 'react'

import {  Box, Button} from '@mui/material';
import Vector1 from './Vector 1.png';
import HiringVector from './Hiring-amico (1) 1.png';
import vector2 from './Vector 2.png';
import vector3 from './Vector 3.png';
import findJob from './findJob.png'
import '../styles/LandingPage.css'



const LandingPage = () => {
  return (
    <div>
        <div>
            <img 
            src={Vector1} alt = ''/>
        </div>
        <div>
            <img 
            src={HiringVector}  alt = ''
            />
        </div>

        <Box className='findJob'>
            <img 
            src={findJob}  alt = ''/>
            <Button className='button-1' sx={{color: "green", backgroundColor: "yellow"}}  href="#/signin" >Get Started</Button>
            
        </Box>
        
        <div className='design'>
            <img className='image'
            src= {vector2} alt = ''
            
            />
            <img className='image'
            src= {vector3} alt = ''/>
        </div>  
    </div>
  )
}

export default LandingPage