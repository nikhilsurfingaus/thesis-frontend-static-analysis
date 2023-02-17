import './App.css';
import { Background } from './components/Background';
import Footer from './components/Footer';
import { Github } from './components/Github';
import HeroSection from './components/HeroSection';
import Navbar from './components/Navbar';
import {Thesis} from './components/Thesis'
import { Tool } from './components/Tool';
import { BrowserRouter } from 'react-router-dom';
import 'animate.css/animate.css'  // you need to require the css somewhere

function App() {
  return (
    <BrowserRouter>
      <div className="App">
          <Navbar />
          <HeroSection />
          <Background />
          <Thesis />
          <Tool />
          <Github />
          <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
