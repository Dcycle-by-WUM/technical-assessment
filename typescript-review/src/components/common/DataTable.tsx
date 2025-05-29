import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/store/store';
import Pagination from './Pagination';
import SortableHeader from './SortableHeader';
import FilterPanel from './FilterPanel';
import ExportButton from './ExportButton';
import Loading from './Loading';
import ErrorDisplay from './ErrorDisplay';

// Any types used extensively
type ColumnDefinition = {
  id: string;
  label: string;
  accessor: (item: any) => any;
  sortable?: boolean;
  filterable?: boolean;
  width?: string;
  cellRenderer?: (value: any, row: any) => React.ReactNode;
};

interface DataTableProps {
  data: any[];
  columns: ColumnDefinition[];
  title?: string;
  loading?: boolean;
  error?: string | null;
  pageSize?: number;
  onRowClick?: (row: any) => void;
  selectable?: boolean;
  exportable?: boolean;
  filterableColumns?: string[];
}

// Component with too many responsibilities - filtering, sorting, pagination, export
const DataTable: React.FC<DataTableProps> = ({
  data = [],
  columns,
  title,
  loading = false,
  error = null,
  pageSize = 10,
  onRowClick,
  selectable = false,
  exportable = false,
  filterableColumns = [],
}) => {
  // Mixed state management - component state and Redux
  const [currentPage, setCurrentPage] = useState(1);
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);
  const [selectedRows, setSelectedRows] = useState<string[]>([]);
  const [filters, setFilters] = useState<Record<string, any>>({});
  const [filteredData, setFilteredData] = useState<any[]>(data);
  const uiPreferences = useSelector((state: RootState) => state.settings.uiPreferences);

  // Complex filtering logic directly in component
  useEffect(() => {
    let result = [...data];
    
    // Apply filters
    if (Object.keys(filters).length > 0) {
      result = result.filter((item) => {
        return Object.entries(filters).every(([key, value]) => {
          if (!value) return true;
          const columnDef = columns.find((col) => col.id === key);
          if (!columnDef) return true;
          
          const itemValue = columnDef.accessor(item);
          if (typeof itemValue === 'string') {
            return itemValue.toLowerCase().includes(value.toLowerCase());
          }
          return itemValue === value;
        });
      });
    }
    
    // Apply sorting
    if (sortConfig) {
      result.sort((a, b) => {
        const column = columns.find((col) => col.id === sortConfig.key);
        if (!column) return 0;
        
        const aValue = column.accessor(a);
        const bValue = column.accessor(b);
        
        if (aValue < bValue) {
          return sortConfig.direction === 'asc' ? -1 : 1;
        }
        if (aValue > bValue) {
          return sortConfig.direction === 'asc' ? 1 : -1;
        }
        return 0;
      });
    }
    
    setFilteredData(result);
    // Reset to first page when filters change
    setCurrentPage(1);
  }, [data, filters, sortConfig, columns]);

  // Pagination calculation
  const totalPages = Math.ceil(filteredData.length / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = Math.min(startIndex + pageSize, filteredData.length);
  const currentData = filteredData.slice(startIndex, endIndex);

  const handleSort = (columnId: string) => {
    setSortConfig((prevSortConfig) => {
      if (prevSortConfig && prevSortConfig.key === columnId) {
        return prevSortConfig.direction === 'asc'
          ? { key: columnId, direction: 'desc' }
          : null;
      }
      return { key: columnId, direction: 'asc' };
    });
  };

  const handleFilterChange = (columnId: string, value: any) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      [columnId]: value,
    }));
  };

  const handleSelectAll = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.checked) {
      const allIds = currentData.map((item) => item.id);
      setSelectedRows(allIds);
    } else {
      setSelectedRows([]);
    }
  };

  const handleSelectRow = (event: React.ChangeEvent<HTMLInputElement>, rowId: string) => {
    event.stopPropagation();
    setSelectedRows((prevSelected) => {
      if (prevSelected.includes(rowId)) {
        return prevSelected.filter((id) => id !== rowId);
      } else {
        return [...prevSelected, rowId];
      }
    });
  };

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return <ErrorDisplay error={error} />;
  }

  return (
    <div className={`data-table ${uiPreferences.darkMode ? 'dark-theme' : ''}`}>
      {title && <h2 className="data-table-title">{title}</h2>}
      
      <div className="data-table-toolbar">
        {filterableColumns.length > 0 && (
          <FilterPanel 
            columns={columns.filter((col) => filterableColumns.includes(col.id))} 
            filters={filters} 
            onFilterChange={handleFilterChange} 
          />
        )}
        
        {exportable && (
          <ExportButton data={filteredData} columns={columns} filename={title || 'export'} />
        )}
      </div>
      
      <div className="data-table-container">
        <table>
          <thead>
            <tr>
              {selectable && (
                <th className="selection-cell">
                  <input
                    type="checkbox"
                    checked={selectedRows.length === currentData.length && currentData.length > 0}
                    onChange={handleSelectAll}
                  />
                </th>
              )}
              
              {columns.map((column) => (
                <th 
                  key={column.id} 
                  style={{ width: column.width || 'auto' }}
                >
                  {column.sortable ? (
                    <SortableHeader
                      label={column.label}
                      active={sortConfig?.key === column.id}
                      direction={sortConfig?.direction || 'asc'}
                      onClick={() => handleSort(column.id)}
                    />
                  ) : (
                    column.label
                  )}
                </th>
              ))}
            </tr>
          </thead>
          
          <tbody>
            {currentData.length === 0 ? (
              <tr>
                <td colSpan={columns.length + (selectable ? 1 : 0)} className="no-data">
                  No data available
                </td>
              </tr>
            ) : (
              currentData.map((item, index) => (
                <tr
                  key={item.id || index}
                  onClick={() => onRowClick && onRowClick(item)}
                  className={onRowClick ? 'clickable' : ''}
                >
                  {selectable && (
                    <td className="selection-cell" onClick={(e) => e.stopPropagation()}>
                      <input
                        type="checkbox"
                        checked={selectedRows.includes(item.id)}
                        onChange={(e) => handleSelectRow(e, item.id)}
                      />
                    </td>
                  )}
                  
                  {columns.map((column) => (
                    <td key={`${item.id || index}-${column.id}`}>
                      {column.cellRenderer 
                        ? column.cellRenderer(column.accessor(item), item)
                        : column.accessor(item)}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      
      {totalPages > 1 && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={setCurrentPage}
          totalItems={filteredData.length}
          itemsPerPage={pageSize}
          startIndex={startIndex}
          endIndex={endIndex}
        />
      )}
    </div>
  );
};

export default DataTable;

