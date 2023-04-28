import React from 'react';
import PropTypes from 'prop-types';
import { Box, Checkbox, TableRow, TableCell, TableHead, TableSortLabel, Toolbar, Tooltip, IconButton, Typography, OutlinedInput, InputAdornment } from '@mui/material';

// Label Component
const Label = ({ color, children }) => {
  return (
    <Box
      sx={{
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: '8px',
        minWidth: 72,
        minHeight: 32,
        px: 1,
        color: 'white',
        backgroundColor: color === 'success' ? 'success.main' : 'error.main',
      }}
    >
      {children}
    </Box>
  );
};

Label.propTypes = {
  color: PropTypes.string.isRequired,
  children: PropTypes.node,
};

// Iconify Component
const Iconify = ({ icon, width = 20, sx, ...other }) => (
  <Box component="span" sx={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width, height: width, ...sx }} {...other}>
    <i className={icon} />
  </Box>
);

Iconify.propTypes = {
  sx: PropTypes.object,
  width: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  icon: PropTypes.string.isRequired,
};

// Scrollbar Component
const Scrollbar = ({ children, sx, ...other }) => {
  return (
    <Box sx={{ overflowX: 'auto', ...sx }} {...other}>
      {children}
    </Box>
  );
};

Scrollbar.propTypes = {
  sx: PropTypes.object,
  children: PropTypes.node,
};

const UserListHead = ({
  order,
  orderBy,
  rowCount,
  headLabel,
  numSelected,
  onRequestSort,
  onSelectAllClick,
}) => {
  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property);
  };

  return (
    <TableHead
      sx={{
        bgcolor: "grey.200", // Add this line to set the background color to grey
      }}
    >
      <TableRow>
        <TableCell padding="checkbox">
          <Checkbox
            indeterminate={numSelected > 0 && numSelected < rowCount}
            checked={rowCount > 0 && numSelected === rowCount}
            onChange={onSelectAllClick}
          />
        </TableCell>
        {headLabel.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.alignRight ? "right" : "left"}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              hideSortIcon
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : "asc"}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
};


UserListHead.propTypes = {
  order: PropTypes.oneOf(['asc', 'desc']),
  orderBy: PropTypes.string,
  rowCount: PropTypes.number,
  headLabel: PropTypes.array,
  numSelected: PropTypes.number,
  onRequestSort: PropTypes.func,
  onSelectAllClick: PropTypes.func,
};
const UserListToolbar = ({ numSelected, filterName, onFilterName, backgroundColor }) => {
  return (
    <Toolbar
      sx={{
        height: 96,
        display: 'flex',
        justifyContent: 'space-between',
        padding: 1,
        backgroundColor: 'background.paper', // Add this line to set the background color to white
        ...(numSelected > 0 && {
          color: 'primary.main',
          bgcolor: 'primary.lighter',
        }),
      }}
    >
      {numSelected > 0 ? (
        <Typography component="div" variant="subtitle1">
          {numSelected} selected
        </Typography>
      ) : (
        <OutlinedInput
          value={filterName}
          onChange={onFilterName}
          placeholder="Search applicant..."
          startAdornment={
            <InputAdornment position="start">
              <Iconify icon="eva:search-fill" sx={{ color: 'text.disabled', width: 20, height: 20 }} />
            </InputAdornment>
          }
          sx={{
            width: 240,
            transition: 'all 0.3s',
            '&.Mui-focused': {
              width: 320,
              boxShadow: 8,
            },
            '& fieldset': {
              borderWidth: `1px !important`,
              borderColor: 'rgba(0, 0, 0, 0.23) !important',
            },
          }}
        />
      )}
    </Toolbar>
  );
};

UserListToolbar.propTypes = {
  numSelected: PropTypes.number,
  filterName: PropTypes.string,
  onFilterName: PropTypes.func,
};

    
    export { Label, Iconify, Scrollbar, UserListHead, UserListToolbar };