import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, View, Image } from 'react-native';
import BackgroundImage from './public/smoky-background.png';
import BooksView from './src/components/books-view';

export default function App() {
	return (
		<View style={styles.container}>
			<Image source={BackgroundImage} style={styles.backgroundImage} />
			<BooksView />
			<StatusBar style="light" />
		</View>
	);
}

const styles = StyleSheet.create({
	backgroundImage: {
		flex: 1,
		resizeMode: 'cover', // or 'stretch'
	},
});
