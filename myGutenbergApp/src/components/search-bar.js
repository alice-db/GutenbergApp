import TextField from '@material-ui/core/TextField';
import React from 'react';

const SearchBar = () => {
	return (
		<TextField
			id="standard-full-width"
			// label
			style={{ margin: 8 }}
			placeholder="Search"
			// helperText
			fullWidth
			margin="normal"
			InputLabelProps={{
				shrink: true,
			}}
		/>
	);
};

export default SearchBar;
