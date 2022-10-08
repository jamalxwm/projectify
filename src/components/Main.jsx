import React, { useState } from 'react';
import styles from '../styles/Main.module.css';
import { Button } from '@mui/material';
import spotify from '../assets/media/spotify-32.png';
import Media from 'react-media';
import SignUpDialog from './SignUpDiaglog';

function Main() {
  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div className={styles.absolute}>
      <div className={styles.innerPadding}>
        <div className={styles.container}>
          <Media query={{ minWidth: 992 }}>
            {(matches) =>
              matches ? (
                <h1>The easiest ticket in town</h1>
              ) : (
                <h1>
                  The easiest <br />
                  ticket in town
                </h1>
              )
            }
          </Media>
          <p>
            <strong>Projectify</strong> reveals the top Warehouse Projects for
            you based on your music taste, so you can spend less time deciding
            and more time dancing
          </p>
          <div className={styles.buttonWrapper}>
            <Button
              variant="contained"
              style={{
                backgroundColor: '#1ED760',
                borderRadius: '104px',
                fontFamily: 'GilroyBold',
                letterSpacing: '0.06em',
              }}
              size="large"
              onClick={() => setOpen(true)}
              startIcon={
                <img src={spotify} style={{ width: '24px', height: '24px' }} />
              }
            >
              Connect with Spotify
            </Button>
            <SignUpDialog open={open} handleClickOpen={handleClickOpen} setOpen={setOpen} handleClose={handleClose}/>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Main;
