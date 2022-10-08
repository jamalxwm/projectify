import React from 'react';
import logo from '../assets/media/projectifylogo.svg';
import styles from '../styles/NavBar.module.css';

function NavBar() {
  return (
    <div>
      <div className={styles.container}>
        <img src={logo} className={styles.logo} alt="projectify logo" />
      </div>
    </div>
  );
}

export default NavBar;
