export class SearchModel {
  constructor(public director: string,
              public writer: string,
              public genres: string[],
              public minRatingIMDB: number,
              public year_from: number,
              public year_to: number,
              public principals: string[],
              public title: string,
              public page_size: number,
              public current_page: number
  ) {
  }
}
