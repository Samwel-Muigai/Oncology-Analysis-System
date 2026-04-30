import { Product } from '@/types';

export const products: Product[] = [
  {
    id: 1,
    name: "MacBook Pro 14\" M3",
    price: 1999,
    description: "Experience unparalleled performance with the new M3 chip, 16GB RAM, and 512GB SSD. Perfect for professionals and creatives.",
    category: "Laptops",
    image: "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500",
    stock: 15,
    specifications: {
      "Processor": "Apple M3",
      "RAM": "16GB",
      "Storage": "512GB SSD",
      "Display": "14-inch Liquid Retina XDR"
    }
  },
  {
    id: 2,
    name: "Samsung Galaxy S24 Ultra",
    price: 1199,
    description: "Capture stunning photos with 200MP camera. AI-powered features and S Pen included.",
    category: "Smartphones",
    image: "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=500",
    stock: 25,
    specifications: {
      "Display": "6.8-inch Dynamic AMOLED",
      "Processor": "Snapdragon 8 Gen 3",
      "RAM": "12GB",
      "Storage": "256GB"
    }
  },
  {
    id: 3,
    name: "Sony WH-1000XM5",
    price: 399,
    description: "Industry-leading noise cancellation with exceptional sound quality. 30-hour battery life.",
    category: "Audio",
    image: "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=500",
    stock: 40,
    specifications: {
      "Type": "Over-ear",
      "Battery": "30 hours",
      "Noise Cancellation": "Yes",
      "Connectivity": "Bluetooth 5.2"
    }
  },
  {
    id: 4,
    name: "iPad Pro 12.9\" M2",
    price: 1099,
    description: "The ultimate iPad experience with M2 chip, LiDAR scanner, and ProMotion display.",
    category: "Tablets",
    image: "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500",
    stock: 20,
    specifications: {
      "Display": "12.9-inch Liquid Retina XDR",
      "Processor": "Apple M2",
      "Storage": "128GB",
      "Camera": "12MP + LiDAR"
    }
  },
  {
    id: 5,
    name: "RTX 4080 Graphics Card",
    price: 1199,
    description: "Ultimate 4K gaming performance with DLSS 3 technology and 16GB VRAM.",
    category: "Components",
    image: "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=500",
    stock: 10,
    specifications: {
      "VRAM": "16GB GDDR6X",
      "CUDA Cores": "9728",
      "Ray Tracing": "3rd Generation",
      "Ports": "3x DP, 1x HDMI"
    }
  },
  {
    id: 6,
    name: "Apple Watch Ultra 2",
    price: 799,
    description: "The most rugged Apple Watch with 49mm titanium case and 36-hour battery life.",
    category: "Wearables",
    image: "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=500",
    stock: 30,
    specifications: {
      "Size": "49mm",
      "GPS": "Yes",
      "Water Resistance": "100m",
      "Features": "ECG, Blood Oxygen"
    }
  },
  {
    id: 7,
    name: "Logitech MX Master 3S",
    price: 99,
    description: "Ergonomic wireless mouse with quiet clicks and 8K DPI tracking.",
    category: "Accessories",
    image: "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=500",
    stock: 50,
    specifications: {
      "DPI": "8000",
      "Connectivity": "Bluetooth + USB",
      "Buttons": "7",
      "Battery": "70 days"
    }
  },
  {
    id: 8,
    name: "LG 27\" 4K Monitor",
    price: 449,
    description: "27-inch 4K UHD IPS display with 95% DCI-P3 color coverage.",
    category: "Monitors",
    image: "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500",
    stock: 18,
    specifications: {
      "Resolution": "3840x2160",
      "Refresh Rate": "60Hz",
      "Panel Type": "IPS",
      "Ports": "USB-C, DP, HDMI"
    }
  }
];