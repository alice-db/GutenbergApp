import React from 'react';
import { ListItem, Avatar, Image } from 'react-native-elements';
import { Text } from 'react-native';

const BookView = ({ book, style }) => {
	return (
		<ListItem containerStyle={style}>
			<ListItem.Content>
				<ListItem.Title>
					<Text>{book.title}</Text>
				</ListItem.Title>
				<ListItem.Subtitle>
					<Text>{book.auteurs}</Text>
				</ListItem.Subtitle>
			</ListItem.Content>
		</ListItem>
	);
};

export default BookView;
