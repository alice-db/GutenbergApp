import { StyleSheet } from 'react-native';
import React, { useState, useCallback } from 'react';
import { SearchBar } from 'react-native-elements';

const SearchBookBar = ({ onChange }) => {
	const [inputText, setInputText] = useState('');

	const onInputChange = (value) => {
		setInputText(value);
		onChange(value);
	};

	return (
		<SearchBar
			placeholder="Type Here..."
			onChangeText={onInputChange}
			value={inputText}
		/>
	);
};

export default SearchBookBar;
