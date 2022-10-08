import React, { useState } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

export default function SignUpDialog({open, setOpen, handleClickOpen, handleClose}) {
  

  return (
    <div>
      <Dialog open={open} onClose={handleClose} >
        <DialogTitle style={{ fontFamily: 'GilroyBold', fontSize: '2em' }}>
          Coming soon!
        </DialogTitle>
        <DialogContent>
          <DialogContentText style={{ fontFamily: 'GilroyMedium' }}>
            Enter your email address below to be add to our launch list
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="Email Address"
            type="email"
            fullWidth
            variant="standard"
            inputProps={{ style: { fontFamily: 'GilroyMedium' } }}
            InputLabelProps={{ style: { fontFamily: 'GilroyMedium' } }}
          />
        </DialogContent>
        <DialogActions >
          <Button onClick={handleClose} style={{ fontFamily: 'GilroyMedium' }}>Cancel</Button>
          <Button onClick={handleClose} style={{ fontFamily: 'GilroyBold' }}>Subscribe</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
