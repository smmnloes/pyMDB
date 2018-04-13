export class SearchModel {
  constructor(public director: string,
              public writer: string,
              public genres: string[],
              public rating: number,
              public min_year: number,
              public max_year: number,
              public principal_1: string,
              public principal_2: string,
              public principal_3: string,
  ) {
  }
}
