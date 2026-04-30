import React from 'react';
import Navbar from './Navbar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="bg-dark text-white py-8 mt-16">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-2xl font-bold mb-4">Jontez Empire</h3>
          <p className="text-gray-300">Your premier destination for cutting-edge electronics</p>
          <p className="text-gray-400 text-sm mt-4">© 2024 Jontez Empire. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;