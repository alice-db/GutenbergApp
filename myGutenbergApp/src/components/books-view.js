import React, { useEffect, useState } from 'react';
import { ScrollView, StyleSheet } from 'react-native';
import Pagination from '@material-ui/lab/Pagination';
import BooksList from './books-list';
import SearchBar from './search-bar';

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
	const [foundBook, setFoundBooks] = useState([]);
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
				console.log(response);
				setBooks(response);
				setFoundBooks(response);
				setBooksPagination(response.slice(0, 500));
			})
			.catch((error) => {
				console.error(error);
			});
	};

	const onPaginationChange = (event, page) => {
		setBooksPagination(foundBook.slice(500 * (page - 1), 500 * page));
	};

	const containsAny = (str, items) => {
		for (var i in items) {
			var item = items[i];
			if (str.indexOf(item) > -1) {
				return true;
			}
		}
		return false;
	};

	const onSearchChange = (value) => {
		let searchUrl, options;

		if (value) {
			if (containsAny(value, ['.', '+', '*', '|', '(', ')'])) {
				searchUrl = 'book_regex/';
				// could be get ?
				options = {
					method: 'POST',
					headers: {
						Accept: 'application/json',
						'Content-Type': 'application/json',
					},
					body: { search: value },
				};
			} else {
				searchUrl = 'book_simple/' + value + '/';
				options = {
					method: 'GET',
					headers: {
						Accept: 'application/json',
						'Content-Type': 'application/json',
					},
				};
			}
			fetch(myGutenbergUrl + searchUrl, options)
				.then((response) => {
					return response.json();
				})
				.then((response) => {
					setFoundBooks(response);
					setBooksPagination(response.slice(0, 500));
				})
				.catch((error) => {
					console.error(error);
				});
		} else {
			setFoundBooks(books);
			setBooksPagination(books.slice(0, 500));
		}
	};

	return (
		<>
			<SearchBar onChange={onSearchChange} />
			<ScrollView contentContainerStyle={styles.view}>
				<Pagination
					className={styles.pagination}
					count={10}
					color="secondary"
					onChange={onPaginationChange}
				/>
				<BooksList books={booksPagination} />
			</ScrollView>
		</>
	);
};

export default BooksView;
