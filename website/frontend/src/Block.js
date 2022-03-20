import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Stack from '@mui/material/Stack';
export default function BoxComponent() {
  return (
    <>
        <Container>
            <Stack spacing={2}>
                <Box component="span" sx={{ p: 20, border: '1px solid grey' }} alignItems='center'>
                    <Button>Save</Button>
                </Box>
                <Box component="span" sx={{ p: 20, border: '1px dashed grey' }}>
                    <Button>Save</Button>
                </Box>
                <Box component="span" sx={{ p: 20, border: '1px dashed grey' }}>
                    <Button>Save</Button>
                </Box>
                <Box component="span" sx={{ p: 20, border: '1px dashed grey' }}>
                    <Button>Save</Button>
                </Box>
            </Stack>
        </Container>
    </>
  );
}