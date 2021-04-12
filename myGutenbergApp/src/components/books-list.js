import React from 'react';
import { FlatList } from 'react-native';
import BookView from './book-view';

const BooksList = ({ books, style }) => {
	return (
		<FlatList
			data={books}
			renderItem={({ item }) => (
				<BookView book={item} style={style} />
			)}></FlatList>
	);
};

export default BooksList;
