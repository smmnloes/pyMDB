export class SearchModel {
  constructor(public director: string,
              public writer: string,
              public genres: string[],
              public rating: number,
              public year_from: number,
              public year_to: number,
              public principals: string[]
  ) {
  }
}
