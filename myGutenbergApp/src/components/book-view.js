import React from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';

const BookView = ({ book }) => {
	return (
		<ListItem>
			<ListItemAvatar>
				<Avatar>
					<img src={book.cover} />
				</Avatar>
			</ListItemAvatar>
			<ListItemText primary={book.url} secondary={book.auteurs} />
		</ListItem>
	);
};

export default BookView;
