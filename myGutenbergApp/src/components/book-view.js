import React from 'react';
import { ListItem, Avatar } from 'react-native-elements';
import { Image } from 'react-native';
import { Text } from 'react-native';

const BookView = ({ book, style }) => {
	return (
		<ListItem containerStyle={style}>
			<Avatar>
				<Image source={book.cover} />
			</Avatar>
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
