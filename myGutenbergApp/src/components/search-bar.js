import { StyleSheet, SafeAreaView } from 'react-native';
import React, { useState, useCallback } from 'react';
import DelayInput from 'react-native-debounce-input';

const SearchBookBar = ({ onChange }) => {
	// const [inputText, setInputText] = useState('');

	const onInputChange = (value) => {
		onChange(value);
	};

	return (
		<SafeAreaView>
			<DelayInput
				placeholder="Type Here..."
				onChangeText={onInputChange}
				delayTimeout={900}
				style={{ margin: 10, height: 40, borderColor: 'gray', borderWidth: 1 }}
			/>
		</SafeAreaView>
	);
};

export default SearchBookBar;
