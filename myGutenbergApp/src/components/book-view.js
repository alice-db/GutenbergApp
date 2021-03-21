import React from 'react';
import Paper from '@material-ui/core/Paper';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';

const BookView = ({ book }) => {
	const formatAuthors = (authors) => {
		console.log(authors);
		return authors.reduce((acc, author) => {
			console.log(author);
			return acc + author.name + ' ';
		}, '');
	};

	return (
		<ListItem>
			<ListItemAvatar>
				<Avatar>
					<img src={!!book.formats && book.formats['image/jpeg']} />
				</Avatar>
			</ListItemAvatar>
			<ListItemText
				primary={book.title}
				secondary={formatAuthors(book.authors)}
			/>
		</ListItem>
	);
};

export default BookView;
