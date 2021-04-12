import React, { useEffect, useState } from 'react';
import { StyleSheet, Platform } from 'react-native';
import Pagination from '@material-ui/lab/Pagination';
import BooksList from './books-list';
import SearchBookBar from './search-bar';
import { CheckBox } from 'react-native-elements';

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
	const [booksSuggestions, setBooksSuggestions] = useState([]);
	const [foundBook, setFoundBooks] = useState([]);
	const [booksPagination, setBooksPagination] = useState([]);
	const [checked, setChecked] = useState(false);

	const myGutenbergUrl = 'http://192.168.1.114:8000/';

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
		let searchUrl;

		if (value) {
			if (containsAny(value, ['.', '+', '*', '|', '(', ')'])) {
				searchUrl = 'book_regex/' + value + '/';
			} else {
				searchUrl = 'book_simple/' + value + '/';
			}
			fetch(myGutenbergUrl + searchUrl, {
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
					setFoundBooks(response.resultats);
					setBooksSuggestions(response.suggestions);
					setBooksPagination(response.resultats.slice(0, 500));
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
			<SearchBookBar onChange={onSearchChange} />
			<CheckBox
				center
				title="Toggle Suggestions"
				checked={checked}
				onPress={() => setChecked(!checked)}
			/>
			{checked && (
				<BooksList
					books={booksSuggestions}
					style={{ backgroundColor: 'rgb(237, 237, 237)' }}
				/>
			)}
			{!Platform.OS === 'ios' && !Platform.OS === 'android' && (
				<Pagination
					className={styles.pagination}
					count={10}
					color="secondary"
					onChange={onPaginationChange}
				/>
			)}
			<BooksList books={booksPagination} />
		</>
	);
};

export default BooksView;
