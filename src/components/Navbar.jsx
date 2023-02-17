import { useState } from 'react';
import { AiOutlineClose, AiOutlineMenu } from 'react-icons/ai';
//import { HashLink as Link } from 'react-router-hash-link';
import { Link } from "react-scroll";

const Navbar = () => {
  const [nav, setNav] = useState(false);
  const [activeLink, setActiveLink] = useState('');

  const handleNav = () => {
    setNav(!nav);
  };

  const handleSetActiveLink = (link) => {
    setActiveLink(link);
  };


  return (
    <div className='flex justify-between items-center h-24 w-full mx-auto px-4 text-white bg-black 
    md:sticky md:pl-6 xsm:sticky top-0 z-20'>
      <h1
        className='text-3xl font-bold md:flex items-center hover:text-white hover:cursor-pointer 
        animate__animated animate__rotateInDownLeft animate__delay-1s'
        style={{
          background:
            'linear-gradient(90deg, rgba(78,53,121,1) 18%, rgba(187,12,255,1) 46%, rgba(146,18,159,1) 77%)',
          WebkitBackgroundClip: 'text',
          backgroundClip: 'text',
          color: 'transparent',
        }}
      >
        <Link
          to='home'
          onClick={() => handleSetActiveLink('#home')}
          spy={true}
          smooth={true}
          offset={-70}
          duration={500}
        >
        PySolSweep
        </Link>
      </h1>

      <ul className='text-lg hidden md:flex font-bold font-sans animate__animated animate__fadeIn animate__delay-1s'>
        <Link
          to='home'
          onClick={() => handleSetActiveLink('#home')}
          className={activeLink === '#home' ? 'text-[#A020F0]' : 'text-white'}
          spy={true}
          smooth={true}
          offset={-70}
          duration={500}
        >
          <li className='p-4 hover:text-[#A020F0] hover:cursor-pointer'>Home</li>
        </Link>
        <Link
          to='background'
          onClick={() => handleSetActiveLink('#background')}
          className={
            activeLink === '#background' ? 'text-[#A020F0]' : 'text-white'
          }
          spy={true}
          smooth={true}
          offset={-70}
          duration={500}
        >
          <li className='p-4 hover:text-[#A020F0] hover:cursor-pointer'>
            Background
          </li>
        </Link>
        <Link
          to='report'
          onClick={() => handleSetActiveLink('#report')}
          className={activeLink === '#report' ? 'text-[#A020F0]' : 'text-white'}
          spy={true}
          smooth={true}
          offset={-70}
          duration={500}
        >
          <li className='p-4 hover:text-[#A020F0] hover:cursor-pointer'>Report</li>
        </Link>
        <Link
          to='tool'
          onClick={() => handleSetActiveLink('#tool')}
          className={activeLink === '#tool' ? 'text-[#A020F0]' : 'text-white'}
          spy={true}
          smooth={true}
          offset={-70}
          duration={500}
        >
          <li className='p-4 hover:text-[#A020F0] hover:cursor-pointer'>Tool</li>
        </Link>
        <Link
          to='github'
          onClick={() => handleSetActiveLink('#github')}
          className={activeLink === '#github' ? 'text-[#A020F0]' : 'text-white'}
          spy={true}
          smooth={true}
          offset={-70}
          duration={500}
        >
          <li className='p-4 hover:text-[#A020F0] hover:cursor-pointer'>Github</li>
        </Link>
      </ul>
      <div className='block md:hidden cursor-pointer z-10'>
        <button onClick={handleNav}>
          {nav ? <AiOutlineClose size={30} /> : <AiOutlineMenu size={30} />}
        </button>
      </div>
      <ul className={nav ? 'z-20 fixed left-0 top-0 w-[60%] h-full border-r border-r-gray-900 bg-[#000300] ease-in-out duration-500' : 
      'ease-in-out duration-500 fixed left-[-100%]'}>
        <h1 className='w-full text-3xl font-bold text-[#A020F0] m-4' style={{
          background:
            'linear-gradient(90deg, rgba(78,53,121,1) 18%, rgba(187,12,255,1) 46%, rgba(146,18,159,1) 77%)',
          WebkitBackgroundClip: 'text',
          backgroundClip: 'text',
          color: 'transparent',
        }}>PySolSweep</h1>
        <Link onClick={() => setNav(!nav)} to='home'><li className='p-4 border-b border-[#A020F0] hover:text-[#A020F0] hover:cursor-pointer'>Home</li></Link>
        <Link onClick={() => setNav(!nav)} to='background'><li className='p-4 border-b border-[#A020F0] hover:text-[#A020F0] hover:cursor-pointer'>Background</li></Link>
        <Link onClick={() => setNav(!nav)} to='report'><li className='p-4 border-b border-[#A020F0] hover:text-[#A020F0] hover:cursor-pointer'>Report</li></Link>
        <Link onClick={() => setNav(!nav)} to='tool'><li className='p-4 border-b border-[#A020F0] hover:text-[#A020F0] hover:cursor-pointer'>Tool</li></Link>
        <Link onClick={() => setNav(!nav)} to='github'><li className='p-4  hover:text-[#A020F0] hover:cursor-pointer'>Github</li></Link>
      </ul>
    </div>
  );
};

export default Navbar;
