import React, { useState } from 'react';
import Link from 'next/link';
import { useCart } from '@/context/CartContext';
import { FiShoppingCart, FiMenu, FiX } from 'react-icons/fi';
import CartSidebar from './CartSidebar';

const Navbar: React.FC = () => {
  const { totalItems } = useCart();
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <>
      <nav className="bg-dark text-white sticky top-0 z-50 shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="text-2xl font-bold hover:text-primary transition">
              Jontez Empire
            </Link>
            
            <div className="hidden md:flex space-x-8">
              <Link href="/" className="hover:text-primary transition">Home</Link>
              <Link href="/#laptops" className="hover:text-primary transition">Laptops</Link>
              <Link href="/#smartphones" className="hover:text-primary transition">Smartphones</Link>
              <Link href="/#audio" className="hover:text-primary transition">Audio</Link>
            </div>
            
            <button
              onClick={() => setIsCartOpen(true)}
              className="relative hover:text-primary transition"
            >
              <FiShoppingCart size={24} />
              {totalItems > 0 && (
                <span className="absolute -top-2 -right-2 bg-secondary text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {totalItems}
                </span>
              )}
            </button>
            
            <button
              className="md:hidden"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
            </button>
          </div>
          
          {isMobileMenuOpen && (
            <div className="md:hidden py-4 space-y-3">
              <Link href="/" className="block hover:text-primary transition">Home</Link>
              <Link href="/#laptops" className="block hover:text-primary transition">Laptops</Link>
              <Link href="/#smartphones" className="block hover:text-primary transition">Smartphones</Link>
              <Link href="/#audio" className="block hover:text-primary transition">Audio</Link>
            </div>
          )}
        </div>
      </nav>
      
      <CartSidebar isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} />
    </>
  );
};

export default Navbar;