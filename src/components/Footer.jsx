import UQ from '../assets/UQ.png';
import Typed from 'react-typed';

const Footer = () => {
  return (
    <>
      <hr className="text-white mx-0" />
      <section className="bg-black">
        <div className="max-w-lg bg-[#A020F0] px-4 pt-24 pb-12 mx-auto md:max-w-none md:text-center">
          <h1 className="text-3xl font-extrabold leading-10 tracking-tight text-white sm:leading-none md:text-6xl lg:text-5xl">
            <span className="block text-2xl mb-2">UQ Thesis Project</span>
            <span className="inline-block bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-pink-200 to-purple-400">
                <Typed
              className='md:text-5xl sm:text-4xl text-xl font-bold md:pl-4 pl-2'
                strings={['"Scientia Ac Labore"']}
                typeSpeed={120}
                backSpeed={140}
                loop
              />
            </span>
          </h1>
          <div className="mx-auto rounded-lg font-black mt-5 text-zinc-400 md:mt-12 md:max-w-lg text-center lg:text-lg">
            <a href="https://itee.uq.edu.au/" target="_blank" rel="noreferrer">
              <button className="bg-tkb border text-sm text-white py-3 px-7 rounded-full font-bold hover:bg-white hover:text-black hover:border-black">
                Learn More
              </button>
            </a>
          </div>
        </div>
      </section>

      <hr className="text-white mx-0" />
      <footer className="bg-black pb-5">
        <div className="max-w-screen-xl px-4 pt-8 mx-auto sm:px-6 lg:px-8 text-white">
          <div className="flex flex-col items-center justify-center md:flex-row md:justify-start">
            <img className="rounded-full" alt="UQ logo" src={UQ} width="50" height="50" />
            <p className="mt-4 text-sm text-center md:text-left md:pl-4 md:mt-0 text-gray-400">
              University Of Queensland (2022), School of Information Technology and Electrical Engineering
            </p>
          </div>
        </div>
      </footer>
    </>
  );
};

export default Footer;
