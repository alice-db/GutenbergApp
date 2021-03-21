import React, { useEffect, useState } from 'react';
import List from '@material-ui/core/List';
import BookView from './book-view';

const BooksMasonry = () => {
	const [books, setBooks] = useState({});

	useEffect(() => {
		getAllBooks();
	}, []);

	const getAllBooks = () => {
		fetch('http://gutendex.com/books', {
			method: 'GET',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
			},
		})
			.then((response) => {
				return response.json();
			})
			.then((response) => {
				console.log(response);
				setBooks(response);
			})
			.catch((error) => {
				console.error(error);
			});
	};

	return (
		<List>
			{!!books.results &&
				books.results.map((book) => {
					return <BookView book={book} />;
				})}
		</List>
	);
};

export default BooksMasonry;
