import { useRouter } from 'next/router';
import Layout from '@/components/Layout';
import { products } from '@/data/products';
import { useCart } from '@/context/CartContext';
import { FiShoppingCart, FiCheck } from 'react-icons/fi';

export default function ProductPage() {
  const router = useRouter();
  const { id } = router.query;
  const { addToCart } = useCart();
  
  const product = products.find(p => p.id === Number(id));

  if (!product) {
    return (
      <Layout>
        <div className="text-center py-12">
          <h1 className="text-2xl font-bold text-dark">Product not found</h1>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-2 gap-8">
          {/* Product Image */}
          <div className="rounded-xl overflow-hidden shadow-lg">
            <img 
              src={product.image} 
              alt={product.name}
              className="w-full h-auto object-cover"
            />
          </div>

          {/* Product Info */}
          <div>
            <h1 className="text-3xl font-bold text-dark mb-2">{product.name}</h1>
            <p className="text-gray-600 mb-4">{product.category}</p>
            
            <div className="mb-6">
              <span className="text-4xl font-bold text-primary">${product.price}</span>
              {product.stock > 0 ? (
                <span className="ml-4 text-green-600 inline-flex items-center gap-1">
                  <FiCheck /> In Stock
                </span>
              ) : (
                <span className="ml-4 text-red-600">Out of Stock</span>
              )}
            </div>

            <p className="text-gray-700 mb-6 leading-relaxed">
              {product.description}
            </p>

            <button
              onClick={() => addToCart(product)}
              disabled={product.stock === 0}
              className={`btn-primary flex items-center gap-2 w-full md:w-auto justify-center ${
                product.stock === 0 ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              <FiShoppingCart size={20} />
              Add to Cart
            </button>

            {/* Specifications */}
            <div className="mt-8">
              <h2 className="text-xl font-bold text-dark mb-4">Specifications</h2>
              <div className="bg-gray-50 rounded-lg p-4">
                {Object.entries(product.specifications).map(([key, value]) => (
                  <div key={key} className="flex py-2 border-b last:border-0">
                    <span className="font-semibold w-32">{key}:</span>
                    <span className="text-gray-700">{value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}