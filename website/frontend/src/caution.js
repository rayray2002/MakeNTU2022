import styled from 'styled-components';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { Button } from '@mui/material';
const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;
const Caution = ()=>{
    return(
        <Wrapper>
            <Box sx={{bgcolor: 'background.paper', borderColor: 'error.main' , borderRadius: 10}}>
                <Typography>您的B電器使用......</Typography>
                <Button variant='contained' color='error'>確認</Button>
            </Box>
        </Wrapper>
    )
}
export default Caution