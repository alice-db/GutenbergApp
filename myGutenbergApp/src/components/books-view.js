import React, { useEffect, useState } from 'react';
import BooksList from './books-list';
import SearchBookBar from './search-bar';
import { CheckBox } from 'react-native-elements';

const BooksView = () => {
	const [books, setBooks] = useState([]);
	const [booksSuggestions, setBooksSuggestions] = useState([]);
	const [foundBook, setFoundBooks] = useState([]);
	const [booksPagination, setBooksPagination] = useState([]);
	const [checked, setChecked] = useState(false);

	// add here ipv6/4 address of server
	const myGutenbergUrl = '';

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
				//setBooksPagination(response.slice(0, 500));
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
		console.log(value);
		if (value) {
			if (containsAny(value, ['.', '+', '*', '|', '(', ')'])) {
				searchUrl = 'book_regex/' + value + '/';
			} else {
				searchUrl = 'book_simple/' + value.toLowerCase() + '/';
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
					console.log('wtf: ' + response);
					setFoundBooks(response.resultats);
					setBooksSuggestions(response.suggestions);
					//setBooksPagination(response.resultats.slice(0, 500));
				})
				.catch((error) => {
					console.error(error);
				});
		} else {
			setFoundBooks(books);
			//setBooksPagination(books.slice(0, 500));
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
			<BooksList books={foundBook} />
		</>
	);
};

export default BooksView;
