import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, View } from 'react-native';
import BackgroundImage from './public/smoky-background.png';
import BooksView from './src/components/books-view';

export default function App() {
	return (
		<View style={styles.container}>
			<BooksView />
			<StatusBar style="light" />
		</View>
	);
}

const styles = StyleSheet.create({
	container: {
		backgroundImage: `url(${BackgroundImage})`,
	},
});
