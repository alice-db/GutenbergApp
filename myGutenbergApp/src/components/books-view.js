import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet } from 'react-native';
import Pagination from '@material-ui/lab/Pagination';
import BooksList from './books-list';

const styles = StyleSheet.create({
	view: {
		height: window.innerHeight,
	},
	pagination: {
		display: 'flex',
		justifyContent: 'center',
	},
});

const BooksView = () => {
	const [books, setBooks] = useState([]);
	const [booksPagination, setBooksPagination] = useState([]);

	const myGutenbergUrl = 'http://127.0.0.1:8000/';

	useEffect(() => {
		getAllBooks();
	}, []);

	const getAllBooks = () => {
		fetch(myGutenbergUrl + 'books/', {
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
				console.log('fetched: ' + response);
				setBooks(response);
				setBooksPagination(response.slice(0, 500));
			})
			.catch((error) => {
				console.error(error);
			});
	};

	const onPaginationChange = (event, page) => {
		setBooksPagination(books.slice(500 * (page - 1), 500 * page));
	};

	return (
		<ScrollView contentContainerStyle={styles.view}>
			<Pagination
				className={styles.pagination}
				count={10}
				color="secondary"
				onChange={onPaginationChange}
			/>
			<BooksList books={booksPagination} />
		</ScrollView>
	);
};

export default BooksView;
