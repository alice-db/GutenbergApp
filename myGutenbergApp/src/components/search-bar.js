import TextField from '@material-ui/core/TextField';
import React from 'react';

const SearchBar = ({ onChange }) => {
	const onInputChange = (event) => {
		let value = event.target && event.target.value;
		onChange(value);
	};

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
			onChange={onInputChange}
		/>
	);
};

export default SearchBar;
