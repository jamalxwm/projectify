import React, { useState } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Alert from '@mui/material/Alert';
import Stack from '@mui/material/Stack';
import emailjs from '@emailjs/browser';
import { Collapse } from '@mui/material';

export default function SignUpDialog({ open, setOpen, handleClose }) {
  const [email, setEmail] = useState('');
  const [sendDisabled, setSendDisabled] = useState(true);
  const [successAlertOpen, setSuccessAlertOpen] = useState(false);
  const templateParams = {
    from_email: email,
  };

  function isValidEmail(email) {
    setSendDisabled(!/\S+@\S+\.\S+/.test(email));
  }

  const handleSubmit = (e) => {
    e.preventDefault();

    emailjs
      .send(
        process.env.REACT_APP_SERVICE_ID,
        process.env.REACT_APP_TEMPLATE_ID,
        templateParams,
        process.env.REACT_APP_PUBLIC_KEY
      )
      .then(() => {
        setOpen(false);
        setEmail('');
        setSuccessAlertOpen(true);
      })
      .catch(alert('Something went wrong. Try again.'));
  };

  return (
    <div>
      <Stack
        sx={{ width: '100%', position: 'fixed', top: 0, left: 0 }}
        spacing={2}
      >
        <Collapse in={successAlertOpen}>
          <Alert
            onClose={() => {
              setSuccessAlertOpen(false);
            }}
            sx={{ margin: 2 }}
          >
            Got it! Get your glad rags ready 💃
          </Alert>
        </Collapse>
      </Stack>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle style={{ fontFamily: 'GilroyBold', fontSize: '2em' }}>
          Coming soon!
        </DialogTitle>
        <DialogContent>
          <DialogContentText style={{ fontFamily: 'GilroyMedium' }}>
            Enter your email address below to get notified when we launch
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="email"
            label="Email Address"
            type="email"
            value={email}
            fullWidth
            variant="standard"
            onChange={(e) => {
              setEmail(e.target.value);
              isValidEmail(e.target.value);
            }}
            inputProps={{ style: { fontFamily: 'GilroyMedium' } }}
            InputLabelProps={{ style: { fontFamily: 'GilroyMedium' } }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} style={{ fontFamily: 'GilroyMedium' }}>
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={sendDisabled}
            style={{ fontFamily: 'GilroyBold' }}
          >
            Subscribe
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
