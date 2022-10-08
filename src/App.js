import './App.css';
import VideoHeader from './components/VideoHeader';
import NavBar from './components/NavBar';
import Main from './components/Main';
import SignUpDialog from './components/SignUpDiaglog';


function App() {
  return (
    <div className="App">
      <NavBar/>
      <VideoHeader/>
      <Main/>
      <SignUpDialog/>
    </div>
  );
}

export default App;
