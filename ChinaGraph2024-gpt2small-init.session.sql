CREATE TABLE IF NOT EXISTS `topics` (
  `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
  `title` TEXT NOT NULL,
  `top_words` TEXT NOT NULL DEFAULT '[]' -- JSON text, array of strings
);
INSERT INTO `topics` VALUES (-1, 'No topic', '[]');
CREATE TABLE IF NOT EXISTS `neurons` (
  `id` TEXT PRIMARY KEY NOT NULL UNIQUE, -- L + `layer_index` + N + `neuron_index` e.g. L01N0234
  `layer_index` INTEGER NOT NULL,
  `neuron_index` INTEGER NOT NULL,
  `explanation_text` TEXT NOT NULL,
  `explanation_embedding` TEXT NOT NULL DEFAULT '[]', -- JSON text, array of floats
  `explanation_topic_id` INTEGER NOT NULL DEFAULT -1,
  `explanation_ev_correlation_score` REAL NOT NULL,
  `explanation_rsquared_score` REAL NOT NULL,
  `explanation_absolute_dev_explained_score` REAL NOT NULL,
  `activation_mean` REAL NOT NULL,
  `activation_variance` REAL NOT NULL,
  `activation_skewness` REAL NOT NULL,
  `activation_kurtosis` REAL NOT NULL,
  FOREIGN KEY(`explanation_topic_id`) REFERENCES `topics`(`id`)
);
CREATE TABLE IF NOT EXISTS `activations` (
  `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
  `neuron_id` TEXT NOT NULL,
  `category` TEXT NOT NULL, -- "random" | "top"
  `tokens` TEXT NOT NULL, -- JSON text, array of strings
  `activation_values` TEXT NOT NULL, -- JSON text, array of floats
  FOREIGN KEY(`neuron_id`) REFERENCES `neurons`(`id`)
);