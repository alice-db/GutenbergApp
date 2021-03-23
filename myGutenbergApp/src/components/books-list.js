import React from 'react';
import List from '@material-ui/core/List';
import BookView from './book-view';

const BooksList = ({ books }) => {
	return (
		<List>
			{!!books &&
				books.map((book) => {
					return <BookView book={book} />;
				})}
		</List>
	);
};

export default BooksList;
