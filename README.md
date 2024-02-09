# ScreenQA dataset

This repository contains Screen Question Answering dataset data first described
in the
[ScreenQA: Large-Scale Question-Answer Pairs over Mobile App Screenshots](https://arxiv.org/abs/2209.08199)
paper.

The dataset contains ~86K questions and answers for ~35K screenshots from the
public [Rico](http://www.interactionmining.org/rico.html) dataset. Only the
screenshots with View Hierarchy in sync were used (see section 4.1 of the paper
for more details).

The screenshots are represented by unique image ids, and those should be used to
retrieve the corresponding images and accompanying data from
[Rico](http://www.interactionmining.org/rico.html).

## Data split

All the screenshots are split randomly into a training set, a validation set,
and a test set. This means that while a single screenshot can have multiple
questions and answers, all questions and answers for the same screenshot are in
the same split.

Train, validation and test splits contain 28378 (~80%), 3485 (~10%) and 3489
(~10%) of all screenshots and 68980 (~80%), 8618 (~10%) and 8427 (~10%) of all
questions respectively.

## Data format

Each directory contains ScreenQA data as 3 JSON files, one per each data split.

### `answers_and_bboxes` directory

Each JSON file in this directory contains a list of question-answers pairs. This
data was produced by human raters.

The available keys for each entry are:

*   `image_id` - screenshot identifier in
    [Rico](http://www.interactionmining.org/rico.html) dataset (should be used
    to get image bytes and other information tied to this screenshot).
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

#### Citation

If you use or discuss this dataset in your work, please cite our paper:

```shell
@misc{hsiao2022screenqa,
      title={ScreenQA: Large-Scale Question-Answer Pairs over Mobile App Screenshots},
      author={Yu-Chung Hsiao and Fedir Zubach and Maria Wang and Jindong Chen},
      year={2022},
      eprint={2209.08199},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### `short_answers` directory

Each JSON file in this directory contains a list of question-answers pairs. The
answers data was produced automatically by a model based on the original data
from human raters. This modification of the original ScreenQA dataset was first
described in the
[ScreenAI: A Vision-Language Model for UI and Infographics Understanding](https://arxiv.org/abs/2402.04615)
paper as "ScreenQA Short".

The available keys for each entry are:

*   `image_id` - screenshot identifier in
    [Rico](http://www.interactionmining.org/rico.html) dataset (should be used
    to get image bytes and other information tied to this screenshot).
*   `question` - question about the screen.
*   `ground_truth` - list of short answers to the question.

#### Citation

If you use or discuss this dataset in your work, please cite our paper:

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

## License

Dataset is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Contact us

If you have a technical question regarding the dataset or publication, please
create an issue in this repository.
