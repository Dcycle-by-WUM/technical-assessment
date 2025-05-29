// DataList.tsx - Component with performance issues
import React, { useEffect, useState } from 'react';

interface DataItem {
  id: number;
  title: string;
  description: string;
  status: 'active' | 'inactive' | 'pending';
}

interface DataListProps {
  items?: DataItem[];
  onItemSelect?: (item: DataItem) => void;
}

const DataList: React.FC<DataListProps> = ({ items = [], onItemSelect }) => {
  // Inefficient: Creating new array on every render
  const activeItems = items.filter(item => item.status === 'active');
  
  // Inefficient: Creating a new function on every render
  const handleItemClick = (item: DataItem) => {
    console.log('Item clicked:', item);
    if (onItemSelect) {
      onItemSelect(item);
    }
  };
  
  // Inefficient state updates in useEffect
  const [filteredItems, setFilteredItems] = useState<DataItem[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Performance issue: Expensive operation on every render without dependencies
  useEffect(() => {
    console.log('Filtering items...');
    
    // Expensive operation that runs on every render
    const result = items.filter(item => 
      item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.description.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    setFilteredItems(result);
  });  // Missing dependency array
  
  // Inefficient: Creating objects in render
  const itemStyle = {
    border: '1px solid #ccc',
    margin: '10px 0',
    padding: '10px',
    borderRadius: '4px',
  };
  
  // Performance issue: Unnecessary inline CSS
  return (
    <div style={{ width: '100%', maxWidth: '800px', margin: '0 auto' }}>
      <h2>Data List ({items.length} items)</h2>
      
      <input 
        type="text" 
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search items..."
        style={{ width: '100%', padding: '8px', marginBottom: '20px' }}
      />
      
      {/* Inefficient: Unnecessarily complex rendering logic */}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {filteredItems.map((item) => {
          // Inline function created on each render
          const getStatusColor = () => {
            switch(item.status) {
              case 'active': return 'green';
              case 'inactive': return 'red';
              case 'pending': return 'orange';
              default: return 'gray';
            }
          };
          
          return (
            <li 
              key={item.id} 
              style={{
                ...itemStyle,
                borderLeft: `4px solid ${getStatusColor()}`,
              }}
              onClick={() => handleItemClick(item)}
            >
              <h3>{item.title}</h3>
              <p>{item.description}</p>
              <span style={{ 
                display: 'inline-block',
                padding: '4px 8px',
                background: getStatusColor(),
                color: 'white',
                borderRadius: '4px',
              }}>
                {item.status}
              </span>
            </li>
          );
        })}
      </ul>
      
      {/* Accessibility issue: No feedback for empty state */}
      {filteredItems.length === 0 && (
        <div style={{ color: '#666', textAlign: 'center' }}>
          No items found
        </div>
      )}
    </div>
  );
};

export default DataList;

