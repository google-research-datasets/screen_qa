# ScreenQA datasets

This repository contains Screen Question Answering datasets data. The datasets
are meant to be used as benchmarks for screen content understanding via question
answering.

The datasets are based on the screenshots from the public
[Rico](http://www.interactionmining.org/rico.html) dataset. The screenshots are
represented by unique image ids, and those should be used to retrieve the
corresponding images and accompanying data from
[Rico](http://www.interactionmining.org/rico.html).

There are currently 3 datasets available here:

*   [ScreenQA](#screenqa) (original).
*   [ScreenQA Short](#screenqa-short).
*   [ComplexQA](#complexqa).

See also a related
[Screen Annotation](https://github.com/google-research-datasets/screen_annotation)
dataset.

## Datasets

### ScreenQA

The dataset contains ~86K questions and answers for ~35K screenshots from the
public [Rico](http://www.interactionmining.org/rico.html) dataset. Only the
screenshots with View Hierarchy in sync were used (see section 4.1 of the
[paper](https://arxiv.org/abs/2209.08199) for more details). This data was
produced by human raters.

All the screenshots are split randomly into a training set, a validation set,
and a test set. This means that while a single screenshot can have multiple
questions and answers, all questions and answers for the same screenshot are in
the same split.

Train, validation and test splits contain 28,378 (~80%), 3,485 (~10%) and 3,489
(~10%) of all screenshots and 68,951 (~80%), 8,614 (~10%) and 8,419 (~10%) of
all questions respectively.

You can find the dataset in the
[`answers_and_bboxes`](https://github.com/google-research-datasets/screen_qa/tree/main/answers_and_bboxes)
directory. It contains ScreenQA data as 3 JSON files, one per each data split.
Each JSON file contains a list of question-answers pairs.

The available keys for each entry are:

*   `image_id` - screenshot identifier in
    [Rico](http://www.interactionmining.org/rico.html) dataset (should be used
    to get image bytes and other information tied to this screenshot).
*   `image_width` - width of the screenshot.
*   `image_height` - height of the screenshot.
*   `question` - question about the screen.
*   `ground_truth` - list of information about the answer to the question, each
    element from a different human rater. Each contains:
    *   `full_answer` - answer to the question as a full sentence.
    *   `ui_elements` - list of elements on the screenshot that contain the
        answer and together with the question are used to produce the answer as
        a full sentence. Each element contains:
        *   `text` - text description of the element (usually the text inside
            the selected area, if available; for icons it is a description of
            the icon, e.g. “4.5 stars”, “home”, “on” for selected
            checkbox/radiobutton and “off” for unselected).
        *   `bounds` - an array of 4 integers representing left, top, right and
            bottom pixel coordinates of the element.
        *   `vh_index` - either `-1` if the element was drawn by the rater
            manually, or non-negative integer representing the index of the
            element in the View Hierarchy tree depth-first traversal (starting
            from 0) if the element is one of the View Hierarchy elements.

### ScreenQA Short

This is a modification of the original ScreenQA dataset. It contains the same
set of questions for the same screenshots in each of the train, validation and
test splits. The answers data was produced automatically by a model based on the
original data from human raters.

You can find the dataset in the
[`short_answers`](https://github.com/google-research-datasets/screen_qa/tree/main/short_answers)
directory. It contains 3 JSON files, one for each data split. Each JSON file
contains a list of question-answers pairs.

The available keys for each entry are:

*   `image_id` - screenshot identifier in
    [Rico](http://www.interactionmining.org/rico.html) dataset (should be used
    to get image bytes and other information tied to this screenshot).
*   `question` - question about the screen.
*   `ground_truth` - list of short answers to the question.

### ComplexQA

This is an extension/alternative to the ScreenQA Short dataset containing
questions and answers mainly focused on counting, arithmetic, and comparison
operations requiring information from more than one part of the screen. It
contains 11,781 question-answer pairs. The data was produced automatically by a
model based on the screen information and validated by human raters.

You can find the dataset in the
[`complex_qa`](https://github.com/google-research-datasets/screen_qa/tree/main/complex_qa)
directory. It contains a `data.json` JSON file with a list of question-answer
pairs.

The available keys for each entry are:

*   `image_id` - screenshot identifier in
    [Rico](http://www.interactionmining.org/rico.html) dataset (should be used
    to get image bytes and other information tied to this screenshot).
*   `question` - question about the screen.
*   `ground_truth` - list of short answers to the question (current version
    contains only one answer though).

## Papers

### [ScreenQA: Large-Scale Question-Answer Pairs over Mobile App Screenshots](https://arxiv.org/abs/2209.08199)

This paper describes the ScreenQA dataset (both [original](#screenqa) and
[short](#screenqa-short)).

If you use or discuss this dataset in your work, please cite our paper:

```shell
@misc{hsiao2024screenqa,
      title={ScreenQA: Large-Scale Question-Answer Pairs over Mobile App Screenshots},
      author={Yu-Chung Hsiao and Fedir Zubach and Gilles Baechler and Victor C{\u a}rbune and Jason Lin and Maria Wang and Srinivas Sunkara and Yun Zhu and Jindong Chen},
      year={2024},
      eprint={2209.08199},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### [ScreenAI: A Vision-Language Model for UI and Infographics Understanding](https://arxiv.org/abs/2402.04615)

This paper describes 2 datasets:

*   [ComplexQA](#complexqa).
*   [Screen Annotation](https://github.com/google-research-datasets/screen_annotation)
    (located in a different repository).

If you use or discuss any of those 2 datasets in your work, please cite our
paper:

```shell
@misc{baechler2024screenai,
      title={ScreenAI: A Vision-Language Model for UI and Infographics Understanding},
      author={Gilles Baechler and Srinivas Sunkara and Maria Wang and Fedir Zubach and Hassan Mansoor and Vincent Etter and Victor Cărbune and Jason Lin and Jindong Chen and Abhanshu Sharma},
      year={2024},
      eprint={2402.04615},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

## Code

The
[`code`](https://github.com/google-research-datasets/screen_qa/tree/main/code)
directory contains `metrics.py` file with functions to compute metrics for
SQA-S, SQA-UIC and SQA-UIC-BB task (see details about the different ScreenQA
tasks in the
[paper](#screenqa-large-scale-question-answer-pairs-over-mobile-app-screenshots)).
For the SQA-L task see [implementation](https://pypi.org/project/rouge-score/)
of the ROUGE metric ([paper](https://aclanthology.org/W04-1013/)).

## License

Dataset is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Contact us

If you have a technical question regarding the dataset or publication, please
create an issue in this repository.
