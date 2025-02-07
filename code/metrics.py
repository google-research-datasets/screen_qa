"""Copyright 2025 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import collections
import re
import string

import numpy as np
import scipy.optimize


NO_ANSWER = "<no answer>"


def sqa_s_metrics(prediction, ground_truths):
  """Computes SQA-S metrics for a single prediction.

  Args:
    prediction: The model prediction.
    ground_truths: The list of ground truth answers.

  Returns:
    A tuple of (Exact Match, F1) metrics after SQuAD preprocessing.
  """
  if prediction == NO_ANSWER:
    if any(gt == NO_ANSWER for gt in ground_truths):
      return 1, 1
    else:
      return 0, 0
  ground_truths = [gt for gt in ground_truths if gt != NO_ANSWER]
  if not ground_truths:
    return 0, 0
  prediction = normalize_squad(prediction)
  ground_truths = [normalize_squad(gt) for gt in ground_truths]
  prediction_tokens = prediction.split()
  exact_match = 1 if prediction in ground_truths else 0
  f1 = max([f1_score(prediction_tokens, gt.split()) for gt in ground_truths])
  return exact_match, f1


def sqa_uic_metrics(prediction, ground_truths):
  """Computes SQA-UIC metrics for a single prediction.

  Args:
    prediction: The model prediction (parsed into a list of UI elements).
    ground_truths: The list of ground truth answers.

  Returns:
    A tuple of (Exact Match, F1) metrics for lists (without UI content
    preprocessing).
  """
  if not prediction:
    if any(not gt for gt in ground_truths):
      return 1, 1
    else:
      return 0, 0
  ground_truths = [gt for gt in ground_truths if gt]
  if not ground_truths:
    return 0, 0
  exact_match = (1 if prediction in ground_truths else 0)
  f1 = max([f1_score(prediction, gt) for gt in ground_truths])
  return exact_match, f1


def sqa_uic_bb_metrics(prediction, ground_truths, iou_threshold=0.1):
  """Computes SQA-UIC-BB metrics for a single prediction.

  Args:
    prediction: The model prediction.
    ground_truths: The list of ground truth answers.
    iou_threshold: IoU threshold for bounding boxes matching.

  Returns:
    A tuple of (BBox-F1@IoU, EM@IoU, F1@IoU) metrics for lists (without UI
    content preprocessing).
  """
  if not prediction:
    if any(not gt for gt in ground_truths):
      return 1, 1, 1
    else:
      return 0, 0, 0
  ground_truths = [gt for gt in ground_truths if gt]
  if not ground_truths:
    return 0, 0, 0
  bbox_f1 = max([
      uic_bb_f1_score(
          [bbox for bbox, _ in prediction],
          [bbox for bbox, _ in gt],
          score_func=iou,
          threshold=iou_threshold,
      )
      for gt in ground_truths
  ])
  exact_match = any(uic_bb_exact_match(prediction, gt) for gt in ground_truths)
  f1 = max([
      uic_bb_f1_score(
          prediction,
          gt,
          score_func=lambda x, y: (iou(x[0], y[0]) if x[1] == y[1] else 0),
          threshold=iou_threshold,
      )
      for gt in ground_truths
  ])
  return bbox_f1, 1 if exact_match else 0, f1


def normalize_squad(text):
  """Lower text and remove punctuation, articles and extra whitespace."""

  def remove_articles(s):
    return re.sub(r"\b(a|an|the)\b", " ", s)

  def replace_punctuation(s, punc_repl):
    return "".join(punc_repl if ch in string.punctuation else ch for ch in s)

  def white_space_fix(s):
    return " ".join(s.split())

  text = text.lower()
  text = replace_punctuation(text, punc_repl="")
  text = remove_articles(text)
  text = white_space_fix(text)
  return text


def f1_score(prediction_tokens, ground_truth_tokens):
  """Computes the F1 score between prediction and ground_truth.

  Args:
    prediction_tokens: A list of tokens in the prediction.
    ground_truth_tokens: A list of tokens in the ground truth.

  Returns:
    The F1 score between prediction and ground_truth.
  """
  common = collections.Counter(prediction_tokens) & collections.Counter(
      ground_truth_tokens
  )
  num_same = sum(common.values())
  if num_same == 0:
    return 0
  precision = 1.0 * num_same / len(prediction_tokens)
  recall = 1.0 * num_same / len(ground_truth_tokens)
  f1 = (2 * precision * recall) / (precision + recall)
  return f1


def iou(bbox1, bbox2):
  """Computes the intersection over union of two bounding boxes.

  Args:
    bbox1: The first bounding box as a tuple of (ymin, xmin, ymax, xmax).
    bbox2: The second bounding box as a tuple of (ymin, xmin, ymax, xmax).

  Returns:
    The intersection over union of the two bounding boxes.
  """
  ymin = max(bbox1[0], bbox2[0])
  xmin = max(bbox1[1], bbox2[1])
  ymax = min(bbox1[2], bbox2[2])
  xmax = min(bbox1[3], bbox2[3])
  intersection_area = max(0, xmax - xmin) * max(0, ymax - ymin)
  if intersection_area == 0:
    return 0
  bbox1_area = (bbox1[3] - bbox1[1]) * (bbox1[2] - bbox1[0])
  bbox2_area = (bbox2[3] - bbox2[1]) * (bbox2[2] - bbox2[0])
  return intersection_area / (bbox1_area + bbox2_area - intersection_area)


def ui_elements_match(element1, element2, iou_threshold=0.1):
  """Checks if two UI elements match.

  Args:
    element1: The first UI element as a tuple of (bbox, UI content).
    element2: The second UI element as a tuple of (bbox, UI content).
    iou_threshold: IoU threshold for bounding boxes matching.

  Returns:
    True if the two UI elements match, False otherwise.
  """
  bbox1, content1 = element1
  bbox2, content2 = element2
  return content1 == content2 and iou(bbox1, bbox2) >= iou_threshold


def uic_bb_exact_match(elements1, elements2, iou_threshold=0.1):
  """Exact match between two lists of UI elements.

  Args:
    elements1: The first list of UI elements.
    elements2: The second list of UI elements.
    iou_threshold: IoU threshold for bounding boxes matching.

  Returns:
    True if the two lists of UI elements match exactly, False otherwise.
  """
  if len(elements1) != len(elements2):
    return False
  return all(
      ui_elements_match(el1, el2, iou_threshold)
      for el1, el2 in zip(elements1, elements2)
  )


def uic_bb_f1_score(prediction, ground_truth, score_func, threshold):
  """Computes F1 score between two lists of UI elements.

  Args:
    prediction: The model prediction as a list of UI elements.
    ground_truth: The ground truth as a list of UI elements.
    score_func: The scoring function to use for matching UI elements.
    threshold: The minimum value of score_func to consider two elements a match.

  Returns:
    The F1 score between the prediction and the ground truth.
  """
  if not prediction and not ground_truth:
    return 1
  if not prediction or not ground_truth:
    return 0
  # Create cost matrix.
  cost_matrix = np.zeros((len(prediction), len(ground_truth)))
  for i, element1 in enumerate(prediction):
    for j, element2 in enumerate(ground_truth):
      score = score_func(element1, element2)
      cost_matrix[i, j] = score if score >= threshold else 0.0
  # Create matches.
  idxs1, idxs2 = scipy.optimize.linear_sum_assignment(-cost_matrix)
  # Filter out any matches below threshold.
  selected_costs = cost_matrix[idxs1, idxs2]
  valid = selected_costs >= threshold
  matches = len(selected_costs[valid])
  if matches == 0:
    return 0
  precision = 1.0 * matches / len(prediction)
  recall = 1.0 * matches / len(ground_truth)
  f1 = (2 * precision * recall) / (precision + recall)
  return f1
